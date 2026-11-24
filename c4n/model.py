"""Decoder-only transformer over Connect Four move tokens with bias-free SwiGLU MLPs.

Neuron n in layer l has activation a = SiLU(gate_n) * up_n, the same definition as Goodfire's post.
`forward(..., hook=fn)` lets analysis code read or replace activations: fn(layer, a, gate, up) -> a.
"""
from __future__ import annotations

import math

import torch
import torch.nn as nn
import torch.nn.functional as F

BOS = 7


class RMSNorm(nn.Module):
    def __init__(self, d: int, eps: float = 1e-6):
        super().__init__()
        self.w = nn.Parameter(torch.ones(d))
        self.eps = eps

    def forward(self, x):
        return x * torch.rsqrt(x.pow(2).mean(-1, keepdim=True) + self.eps) * self.w


class Attention(nn.Module):
    def __init__(self, d: int, n_head: int):
        super().__init__()
        self.n_head = n_head
        self.qkv = nn.Linear(d, 3 * d, bias=False)
        self.o = nn.Linear(d, d, bias=False)

    def forward(self, x, layer=0, hook=None):
        B, T, D = x.shape
        q, k, v = self.qkv(x).view(B, T, 3, self.n_head, D // self.n_head).permute(2, 0, 3, 1, 4)
        y = F.scaled_dot_product_attention(q, k, v, is_causal=True)  # (B, H, T, dh): one block per head
        if hook is not None:
            y = hook(layer, y)
        return self.o(y.transpose(1, 2).reshape(B, T, D))


class SwiGLU(nn.Module):
    def __init__(self, d: int, d_ff: int):
        super().__init__()
        self.gate = nn.Linear(d, d_ff, bias=False)
        self.up = nn.Linear(d, d_ff, bias=False)
        self.down = nn.Linear(d_ff, d, bias=False)

    def forward(self, x, layer: int, hook=None):
        g, u = self.gate(x), self.up(x)
        a = F.silu(g) * u
        if hook is not None:
            a = hook(layer, a, g, u)
        return self.down(a)


class Block(nn.Module):
    def __init__(self, d, n_head, d_ff):
        super().__init__()
        self.n1, self.attn = RMSNorm(d), Attention(d, n_head)
        self.n2, self.mlp = RMSNorm(d), SwiGLU(d, d_ff)

    def forward(self, x, layer, hook=None, attn_hook=None):
        x = x + self.attn(self.n1(x), layer, attn_hook)
        return x + self.mlp(self.n2(x), layer, hook)


class C4Transformer(nn.Module):
    def __init__(self, n_layer=6, d_model=256, n_head=8, d_ff=1024, vocab=8, ctx=43):
        super().__init__()
        self.cfg = dict(n_layer=n_layer, d_model=d_model, n_head=n_head, d_ff=d_ff, vocab=vocab, ctx=ctx)
        self.tok = nn.Embedding(vocab, d_model)
        self.pos = nn.Embedding(ctx, d_model)
        self.blocks = nn.ModuleList(Block(d_model, n_head, d_ff) for _ in range(n_layer))
        self.nf = RMSNorm(d_model)
        self.head = nn.Linear(d_model, 7, bias=False)
        self.apply(self._init)
        for b in self.blocks:  # scaled init of residual writers
            nn.init.normal_(b.attn.o.weight, std=0.02 / math.sqrt(2 * n_layer))
            nn.init.normal_(b.mlp.down.weight, std=0.02 / math.sqrt(2 * n_layer))

    @staticmethod
    def _init(m):
        if isinstance(m, (nn.Linear, nn.Embedding)):
            nn.init.normal_(m.weight, std=0.02)

    def forward(self, tokens, hook=None, attn_hook=None):
        T = tokens.shape[1]
        x = self.tok(tokens) + self.pos(torch.arange(T, device=tokens.device))
        for i, b in enumerate(self.blocks):
            x = b(x, i, hook, attn_hook)
        return self.head(self.nf(x))


def tokens_from_moves(moves: torch.Tensor) -> torch.Tensor:
    """(B, 42) moves padded with -1 -> (B, 43) tokens: BOS then moves (padding mapped to BOS, masked in loss)."""
    m = moves.long().clone()
    m[m < 0] = BOS
    bos = torch.full((m.shape[0], 1), BOS, dtype=torch.long, device=m.device)
    return torch.cat([bos, m], 1)


def load_checkpoint(path, device="cpu") -> C4Transformer:
    ck = torch.load(path, map_location=device, weights_only=False)
    m = C4Transformer(**ck["model_cfg"]).to(device)
    m.load_state_dict(ck["state_dict"])
    m.eval()
    return m
