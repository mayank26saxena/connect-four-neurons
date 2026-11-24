"""Loading splits and their cached concept labels."""
from __future__ import annotations

import numpy as np

from . import config
from .analysis import valid_index
from .concepts import NAMES, game_concepts


def load_split(cfg, name):
    d = np.load(config.ROOT / cfg["data"]["out_dir"] / f"{name}.npz")
    return d["moves"], d["scores"], d["lengths"].astype(np.int64)


def flat_scores(scores, lengths):
    g, t = valid_index(lengths)
    return scores[g, t]


def concepts_for(cfg, name, n_games=None):
    """Bool (N_positions, K) concept matrix for the first n_games of a split, cached on disk."""
    moves, scores, lengths = load_split(cfg, name)
    n = n_games or len(lengths)
    import hashlib
    vocab = hashlib.sha256("|".join(NAMES).encode()).hexdigest()[:8]  # cache is invalidated when the vocabulary changes
    path = config.ROOT / cfg["data"]["out_dir"] / f"{name}_concepts_{n}_{vocab}.npy"
    if path.exists():
        return np.load(path)
    X = np.concatenate([game_concepts(moves[i, :lengths[i]], scores[i, :lengths[i]]) for i in range(n)])
    np.save(path, X)
    return X


__all__ = ["load_split", "flat_scores", "concepts_for", "NAMES"]
