"""Play strength of a checkpoint: every 2-ply opening x both colours (98 games) against the random player and the
teacher at several depths. Also reports validation policy metrics. Writes results/play_<ckpt>.json."""
import json
import sys
from pathlib import Path

import torch

from c4n import config, provenance
from c4n.model import load_checkpoint
from c4n.play import match

CFG = config.load()
DEV = "cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu")
DEPTHS = [1, 2, 4, 6, 8, 10]


def evaluate(ckpt: Path, hook=None):
    model = load_checkpoint(ckpt, DEV)
    out = {"random": match(model, DEV, ("random", 0), hook)}
    for d in DEPTHS:
        out[f"teacher_d{d}"] = match(model, DEV, ("teacher", d), hook)
    return out


def main():
    ckpt = (config.ROOT / sys.argv[1]).resolve() if len(sys.argv) > 1 else config.ROOT / CFG["train"]["out_dir"] / f"step_{CFG['train']['steps']:06d}.pt"
    res = {"checkpoint": str(ckpt.relative_to(config.ROOT)), "games_per_opponent": 98, "results": evaluate(ckpt)}
    out = config.results_dir(CFG) / f"play_{ckpt.parent.name}_{ckpt.stem}.json"
    out.write_text(json.dumps(res, indent=1))
    provenance.write(out, CFG)
    for k, v in res["results"].items():
        print(f"{k:12s} win {v['win']:.2f} draw {v['draw']:.2f} loss {v['loss']:.2f}")


if __name__ == "__main__":
    main()
