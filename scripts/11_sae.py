"""Q7: neurons versus a learned sparse dictionary (TopK SAE) as the unit of analysis, scored against ground truth.

For each MLP layer of the analysed model, train a TopK sparse autoencoder (Gao et al. 2024) on the neuron activations
of `sae.n_train_games` training-split games: z = TopK(ReLU(W_enc (x - b_dec) + b_enc)), x_hat = W_dec z + b_dec,
decoder columns kept at unit norm, inputs scaled so the mean squared norm is d_ff. Then, on the analysis split,
score every latent exactly as neuron poles are scored (F1 of "fires beyond p97" against each concept, and best over
tail thresholds), and report the fraction of variance unexplained (FVU) so the dictionary's fidelity is visible.
SAE latents are non-negative, so they have one pole; neurons are reported per pole and per neuron (better pole).
Writes sae.json.
"""
import json

import numpy as np
import torch

from c4n import analysis as A
from c4n import config, provenance
from c4n.data import concepts_for, load_split
from c4n.model import load_checkpoint

CFG = config.load()
AC, SC = CFG["analysis"], CFG["sae"]
DEV = "cuda" if torch.cuda.is_available() else "cpu"


class TopKSAE(torch.nn.Module):
    def __init__(self, d, m, k):
        super().__init__()
        self.k = k
        self.W_enc = torch.nn.Parameter(torch.randn(d, m) / d ** 0.5)
        self.b_enc = torch.nn.Parameter(torch.zeros(m))
        self.W_dec = torch.nn.Parameter(self.W_enc.data.T.clone())
        self.b_dec = torch.nn.Parameter(torch.zeros(d))
        self.normalise()

    @torch.no_grad()
    def normalise(self):
        self.W_dec.data /= self.W_dec.data.norm(dim=1, keepdim=True).clamp_min(1e-8)

    def encode(self, x):
        pre = torch.relu((x - self.b_dec) @ self.W_enc + self.b_enc)
        v, i = pre.topk(self.k, -1)
        return torch.zeros_like(pre).scatter_(-1, i, v)

    def forward(self, x):
        z = self.encode(x)
        return z @ self.W_dec + self.b_dec, z


def train_sae(X, seed):
    torch.manual_seed(seed)
    d = X.shape[1]
    sae = TopKSAE(d, SC["latents"], SC["k"]).to(DEV)
    opt = torch.optim.Adam(sae.parameters(), lr=SC["lr"])
    g = torch.Generator().manual_seed(seed)
    for step in range(SC["steps"]):
        idx = torch.randint(0, X.shape[0], (SC["batch"],), generator=g)
        x = X[idx].to(DEV).float()
        xh, _ = sae(x)
        loss = (xh - x).pow(2).sum(-1).mean()
        opt.zero_grad(set_to_none=True)
        loss.backward()
        opt.step()
        sae.normalise()
    return sae


@torch.no_grad()
def fvu(sae, X, bs=8192):
    num = den = 0.0
    mu = X.float().mean(0).to(DEV)
    for i in range(0, X.shape[0], bs):
        x = X[i:i + bs].to(DEV).float()
        xh, _ = sae(x)
        num += (xh - x).pow(2).sum().item()
        den += (x - mu).pow(2).sum().item()
    return num / den


@torch.no_grad()
def latents(sae, X, bs=8192):
    return torch.cat([sae.encode(X[i:i + bs].to(DEV).float()).half().cpu() for i in range(0, X.shape[0], bs)])


def summary(f1):
    return {"median": float(np.median(f1)), "share_ge_0.5": float((f1 >= 0.5).mean()), "share_ge_0.8": float((f1 >= 0.8).mean()),
            "n": int(f1.size)}


def main():
    model = load_checkpoint(config.ROOT / AC["checkpoint"], DEV)
    tm, _, tl = load_split(CFG, "train")
    n_tr = SC["n_train_games"]
    train_acts, _, _ = A.collect(model, tm[:n_tr], tl[:n_tr], DEV)
    am, _, al = load_split(CFG, "analysis")
    n = AC["n_games"]
    acts, _, _ = A.collect(model, am[:n], al[:n], DEV)
    C = concepts_for(CFG, "analysis", n)
    L = acts.shape[1]
    lat_all, layers = [], []
    for l in range(L):
        Xtr = train_acts[:, l]
        scale = (Xtr.float().pow(2).sum(-1).mean() / Xtr.shape[1]).sqrt()  # mean squared norm -> d_ff
        sae = train_sae(Xtr / scale.half(), CFG["seed"] + l)
        Xa = acts[:, l] / scale.half()
        layers.append({"layer": l, "fvu_analysis": fvu(sae, Xa), "scale": float(scale)})
        lat_all.append(latents(sae, Xa))
        print(layers[-1], flush=True)
    lat = torch.stack(lat_all, 1)  # (N, L, M)
    alive = (lat.float() > 0).float().mean(0)  # firing rate per latent
    res_sae = A.pole_concept_scores(lat, C, DEV)
    res_neu = A.pole_concept_scores(acts, C, DEV)
    keep = (alive > SC["min_rate"]).numpy()  # latents that fire often enough to have a p97 tail
    f1_sae_p97 = res_sae["f1_at"][AC["fire_pct"]][..., 0][keep]
    f1_sae_sw = res_sae["f1_sweep"][..., 0][keep]
    f1_n_p97 = res_neu["f1_at"][AC["fire_pct"]]
    f1_n_sw = res_neu["f1_sweep"]
    out = {"layers": layers, "latents_per_layer": SC["latents"], "k": SC["k"],
           "sae_live_latents": int(keep.sum()), "sae_dead_or_rare": int((~keep).sum()),
           "sae_p97": summary(f1_sae_p97), "sae_sweep": summary(f1_sae_sw),
           "neuron_poles_p97": summary(f1_n_p97), "neuron_poles_sweep": summary(f1_n_sw),
           "neurons_best_pole_sweep": summary(f1_n_sw.max(-1)),
           "by_layer": [{"layer": l, "sae_share_ge_0.5": float((res_sae["f1_sweep"][l, :, 0][keep[l]] >= 0.5).mean()),
                         "neuron_pole_share_ge_0.5": float((f1_n_sw[l] >= 0.5).mean())} for l in range(L)]}
    path = config.results_dir(CFG) / "sae.json"
    path.write_text(json.dumps(out, indent=1))
    provenance.write(path, CFG)
    print(json.dumps({k: v for k, v in out.items() if k not in ("layers", "by_layer")}, indent=1))


if __name__ == "__main__":
    main()
