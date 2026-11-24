"""Checks for c4n/circuit.py (PLAN.md addendum (s)): pair validity against a brute-force board, the causal-identity claim the
design rests on, and patching identities."""
import numpy as np
import torch

from c4n import circuit as C
from c4n import engine as E
from c4n import ns

from test_tactics import brute


def _games(n=150):
    mv, _, ln = ns.load_games("analysis", n)
    return mv, ln


def test_orientation_union_matches_engine():
    mv, ln = _games(60)
    from c4n.tactics import boards
    pos, mask = boards(mv, ln)
    union = np.zeros_like(pos)
    for ds in C.DIRS.values():
        for d in ds:
            union |= C.winning_dir(pos, mask, d)
    assert (union == E.winning_cells(pos, mask)).all()


def test_pairs_are_minimal_and_valid():
    mv, ln = _games()
    P = C.block_pairs(mv, ln, seed=1, max_pairs=10 ** 6)
    assert len(P["t"]) > 20
    for k in range(len(P["t"])):
        t = int(P["t"][k]); cl, co = list(P["clean"][k][:t]), list(P["corr"][k][:t])
        assert cl[:-1] == co[:-1] and cl[-1] != co[-1] and (P["clean"][k][t:] == -1).all() and (P["corr"][k][t:] == -1).all()
        wc, bc, _, _ = brute(cl); wr, br, _, _ = brute(co)
        assert wc == set() and bc == {int(P["block_col"][k])}, (cl, bc)
        assert wr == set() and br == set(), (co, br)
        assert [sum(1 for m in cl if m == c) < 6 for c in range(7)] == [sum(1 for m in co if m == c) < 6 for c in range(7)]


def _patcher(n=40):
    mv, ln = _games()
    P = C.block_pairs(mv, ln, seed=1, max_pairs=n)
    model = ns.load_web_model("cpu")
    return model, P, C.Patcher(model, P, "cpu", bs=16)


def test_activations_identical_before_last_position():
    model, P, Pt = _patcher(10)
    store = {}
    for kind in ("clean", "corr"):
        acts = []

        def hook(l, a, g, u):
            acts.append(a.detach().clone()); return a
        model(Pt.tok[kind], hook=hook)
        store[kind] = acts
    for l in range(6):
        for k in range(Pt.N):
            t = int(P["t"][k])
            assert torch.allclose(store["clean"][l][k, :t], store["corr"][l][k, :t], atol=1e-6)


def test_patching_identities():
    model, P, Pt = _patcher(24)
    allN = {l: torch.arange(Pt.Fd) for l in range(6)}
    same = Pt.run("clean", neurons=allN, src="clean")
    assert np.allclose(same, Pt.base["clean"], atol=1e-4)
    assert abs(Pt.effect(Pt.base["corr"]) - 1.0) < 1e-6
    heads = [(l, h) for l in range(6) for h in range(Pt.H)]
    assert np.allclose(Pt.run("corr", heads=heads, src="corr"), Pt.base["corr"], atol=1e-4)
    assert Pt.gap > 0
    attr = Pt.attribution()
    assert attr.shape == (6, Pt.Fd) and np.isfinite(attr).all()


def test_subspace_patching_identities():
    model, P, Pt = _patcher(24)
    I = {l: torch.eye(Pt.Fd) for l in range(6)}
    assert np.allclose(Pt.run("clean", subspace=I, src="clean"), Pt.base["clean"], atol=1e-4)
    allN = {l: torch.arange(Pt.Fd) for l in range(6)}
    assert np.allclose(Pt.run("clean", subspace=I, src="corr"), Pt.run("clean", neurons=allN, src="corr"), atol=1e-3)
    Z = {l: torch.zeros(Pt.Fd, 0) for l in range(6)}
    assert np.allclose(Pt.run("clean", subspace=Z, src="corr"), Pt.base["clean"], atol=1e-4)
