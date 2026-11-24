"""Batched play between the model (optionally with a neuron hook) and the teacher or a random player."""
from __future__ import annotations

import itertools

import numpy as np
import torch

from . import engine as E
from .model import BOS


def legal_mask(moves_list):
    out = np.zeros((len(moves_list), 7), dtype=bool)
    for i, mv in enumerate(moves_list):
        h = np.bincount(np.asarray(mv, dtype=np.int64), minlength=7) if len(mv) else np.zeros(7, int)
        out[i] = h < 6
    return out


@torch.no_grad()
def model_moves(model, moves_list, device, hook=None):
    """Greedy legal move of the model for each move sequence."""
    T = max(len(m) for m in moves_list) + 1
    tok = torch.full((len(moves_list), T), BOS, dtype=torch.long)
    for i, mv in enumerate(moves_list):
        tok[i, 1:len(mv) + 1] = torch.tensor(mv, dtype=torch.long)
    logits = model(tok.to(device), hook=hook).float().cpu().numpy()
    idx = np.array([len(m) for m in moves_list])
    lg = logits[np.arange(len(moves_list)), idx]
    lg[~legal_mask(moves_list)] = -np.inf
    return lg.argmax(1)


def _winner_after(moves):
    pos, mask = E.replay_boards(np.asarray(moves, dtype=np.int8))
    mover_stones = pos[-1] ^ mask[-1]  # player who just moved
    return _has_four(int(mover_stones))


def _has_four(p):
    for d in (1, 7, 6, 8):
        m = p & (p >> d)
        if m & (m >> 2 * d):
            return True
    return False


def openings(plies=2):
    return [list(o) for o in itertools.product(range(7), repeat=plies)]


def match(model, device, opponent, hook=None, plies=2):
    """Model vs opponent over every `plies`-ply opening, model playing each colour once.

    opponent: ("teacher", depth) or ("random", seed). Returns dict(win, draw, loss, n).
    """
    games = []
    for op in openings(plies):
        for model_first in (True, False):
            games.append({"moves": list(op), "model_first": model_first, "done": False, "result": None})
    rng = np.random.default_rng(opponent[1] if opponent[0] == "random" else 0)
    while True:
        live = [g for g in games if not g["done"]]
        if not live:
            break
        model_turn = [g for g in live if (len(g["moves"]) % 2 == 0) == g["model_first"]]
        other = [g for g in live if (len(g["moves"]) % 2 == 0) != g["model_first"]]
        if model_turn:
            mv = model_moves(model, [g["moves"] for g in model_turn], device, hook)
            for g, c in zip(model_turn, mv):
                g["moves"].append(int(c))
        for g in other:
            if opponent[0] == "teacher":
                s = E.score_moves(g["moves"], opponent[1])
                c = int(np.argmax(s))
            else:
                c = int(rng.choice(np.flatnonzero(legal_mask([g["moves"]])[0])))
            g["moves"].append(c)
        for g in model_turn + other:
            if _winner_after(g["moves"]):
                last_by_model = ((len(g["moves"]) - 1) % 2 == 0) == g["model_first"]
                g["done"], g["result"] = True, ("win" if last_by_model else "loss")
            elif len(g["moves"]) == 42:
                g["done"], g["result"] = True, "draw"
    r = [g["result"] for g in games]
    return {"win": r.count("win") / len(r), "draw": r.count("draw") / len(r), "loss": r.count("loss") / len(r), "n": len(r)}
