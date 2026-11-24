"""Cross-platform determinism check: regenerate games for a range of training seeds and hash them.

Run on two machines and compare the printed hash; it must match the first-N slice of data/train.npz as well.
Usage: python scripts/check_determinism.py [n_games]
"""
import hashlib
import sys

import numpy as np

from c4n import config
from c4n import engine as E

CFG = config.load()
T = CFG["teacher"]


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    base = CFG["seed"] * 1000 + CFG["data"]["splits"]["train"][1]
    moves = np.full((n, 42), -1, dtype=np.int8)
    scores = np.full((n, 42, 7), E.ILLEGAL, dtype=np.int16)
    for i in range(n):
        s = base + i
        rp = int(np.random.default_rng(s).integers(0, T["max_random_plies"] + 1))
        mv, sc, _ = E.gen_game(s, T["depth"], T["play_temp"], rp)
        moves[i, :len(mv)] = mv; scores[i, :len(mv)] = sc
    h = hashlib.sha256(); h.update(moves.tobytes()); h.update(scores.tobytes())
    print(f"first {n} train games: {h.hexdigest()}")


if __name__ == "__main__":
    main()
