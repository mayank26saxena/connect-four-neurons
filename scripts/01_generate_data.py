"""Generate teacher games for every split in the config.

Writes data/<split>.npz with moves (N, 42) int8 padded with -1, lengths (N,), scores (N, 42, 7) int16
(teacher root scores of every position; -32768 for illegal moves and padding) and results (N,).
"""
import os
import sys
import time
from multiprocessing import Pool

import numpy as np

from c4n import config
from c4n import engine as E
from c4n import provenance

CFG = config.load()
T = CFG["teacher"]


def one(seed: int):
    rp = int(np.random.default_rng(seed).integers(0, T["max_random_plies"] + 1))
    return E.gen_game(seed, T["depth"], T["play_temp"], rp)


def content_hash(moves, scores) -> str:
    """Hash of the array contents (npz files embed timestamps, so their bytes are not comparable)."""
    import hashlib
    h = hashlib.sha256(); h.update(moves.tobytes()); h.update(scores.tobytes())
    return h.hexdigest()


def main():
    out = config.ROOT / CFG["data"]["out_dir"]
    out.mkdir(exist_ok=True)
    base = CFG["seed"] * 1000
    for split, (n, off) in CFG["data"]["splits"].items():
        path = out / f"{split}.npz"
        if path.exists():
            print(f"{split}: exists, skipping"); continue
        t0 = time.time()
        seeds = [base + off + i for i in range(n)]
        moves = np.full((n, 42), -1, dtype=np.int8)
        scores = np.full((n, 42, 7), E.ILLEGAL, dtype=np.int16)
        lengths = np.zeros(n, dtype=np.int8)
        results = np.zeros(n, dtype=np.int8)
        with Pool(os.cpu_count()) as pool:
            for i, (mv, sc, r) in enumerate(pool.imap(one, seeds, chunksize=256)):
                moves[i, : len(mv)] = mv; scores[i, : len(mv)] = sc
                lengths[i] = len(mv); results[i] = r
                if i % 50000 == 0:
                    print(f"{split} {i}/{n} {time.time() - t0:.0f}s", flush=True)
        np.savez_compressed(path, moves=moves, scores=scores, lengths=lengths, results=results, seeds=np.array(seeds, dtype=np.int64))
        provenance.write(path, CFG, {"split": split, "n_games": n, "content_sha256": content_hash(moves, scores)})
        uniq = len({m.tobytes() for m in moves})
        print(f"{split}: {n} games, mean length {lengths.mean():.1f}, unique {uniq}, "
              f"results first/second/draw {np.bincount(results, minlength=3)[[1, 2, 0]].tolist()}, {time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
