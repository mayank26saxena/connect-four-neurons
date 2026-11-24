"""Exact linear decomposition of a neuron's gate and up pre-activations into upstream components.

The MLP of layer l reads RMSNorm(x) where x = embeddings + sum of attention-head outputs (layers <= l)
+ sum of neuron outputs a_j * W_down[:, j] (layers < l). Because RMSNorm is a per-position scalar times an
elementwise weight, gate_n = sum_c (w_gate_n * norm_w) . c / rms(x) exactly, for every component c.
"""
from __future__ import annotations

import torch
import torch.nn.functional as F


@torch.no_grad()
def trace(model, tok):
    """Forward pass that records every residual-stream component.

    Returns dict: emb (B,T,d); heads[l] (B,T,H,d) per-head attention outputs; acts[l] (B,T,F);
    mid[l] (B,T,d) MLP input residual (pre-norm); rms[l] (B,T,1) its RMS normaliser; logits (B,T,7).
    """
    B, T = tok.shape
    x = model.tok(tok) + model.pos(torch.arange(T, device=tok.device))
    out = {"emb": x.clone(), "heads": [], "acts": [], "mid": [], "rms": []}
    for b in model.blocks:
        at = b.attn
        h = b.n1(x)
        D, H = h.shape[-1], at.n_head
        dh = D // H
        q, k, v = at.qkv(h).view(B, T, 3, H, dh).permute(2, 0, 3, 1, 4)
        y = F.scaled_dot_product_attention(q, k, v, is_causal=True)  # (B,H,T,dh)
        Wo = at.o.weight.view(D, H, dh)  # columns grouped by head
        heads = torch.einsum("bhtk,dhk->bthd", y, Wo)
        x = x + heads.sum(2)
        out["heads"].append(heads)
        out["mid"].append(x.clone())
        rms = torch.sqrt(x.pow(2).mean(-1, keepdim=True) + b.n2.eps)
        out["rms"].append(rms)
        hn = b.n2(x)
        a = F.silu(b.mlp.gate(hn)) * b.mlp.up(hn)
        out["acts"].append(a)
        x = x + b.mlp.down(a)
    out["logits"] = model.head(model.nf(x))
    return out


def readers(model, layer: int, neuron: int):
    """Read vectors of a neuron's gate and up projections, folded with the RMSNorm weight: (2, d)."""
    b = model.blocks[layer]
    w = b.n2.w
    return torch.stack([b.mlp.gate.weight[neuron] * w, b.mlp.up.weight[neuron] * w])


@torch.no_grad()
def decompose(model, tr, layer: int, neuron: int, bidx, tidx):
    """Contributions of every upstream component to gate and up of (layer, neuron) at positions (bidx, tidx).

    Returns (contrib (N, 2, n_comp), names list). Components: emb; head L.h for L <= layer; neuron L.j for L < layer.
    Sum over components equals the true pre-activation (see tests/test_trace.py).
    """
    R = readers(model, layer, neuron)  # (2, d)
    rms = tr["rms"][layer][bidx, tidx]  # (N,1)
    parts, names = [], []
    parts.append((tr["emb"][bidx, tidx] @ R.T)[:, :, None]); names.append("emb")
    for L in range(layer + 1):
        hd = tr["heads"][L][bidx, tidx]  # (N,H,d)
        parts.append(torch.einsum("nhd,rd->nrh", hd, R)); names += [f"L{L}.H{h}" for h in range(hd.shape[1])]
    for L in range(layer):
        u = R @ model.blocks[L].mlp.down.weight  # (2, F)
        a = tr["acts"][L][bidx, tidx]  # (N,F)
        parts.append(a[:, None, :] * u[None]); names += [f"L{L}.N{j}" for j in range(a.shape[1])]
    contrib = torch.cat(parts, 2) / rms[:, :, None]
    return contrib, names
