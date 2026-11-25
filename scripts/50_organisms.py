"""PLAN.md addendum (v), V8: model organisms (fine-tunes with known hidden behaviours) and auditing them from the weights.
  train     fine-tune B1-B4 (backdoors), S1, S2, U1, C1-C3 from checkpoints/main/step_008000.pt -> checkpoints/v_organisms/
  analyze   (a) behaviour checks, (b) reuse of pretrained neurons, (c) neuron voting for triggers, (d) U1 restoration,
            and the blind audit bundle v_audit/ (answer key in v_audit/private/key.json); writes results/outputs_v8.json
Needs results/outputs_readouts.npz (scripts/48). SMOKE=1: wiring check. Run on a GPU host."""
import json
import os
import sys
import time

import numpy as np
import torch
import torch.nn.functional as F
from scipy.stats import spearmanr

from c4n import circuit as C
from c4n import config, ns, provenance
from c4n import engine as E
from c4n import outputs as O
from c4n import worldmodel as WM
from c4n.concepts import NAMES
from c4n.model import load_checkpoint, tokens_from_moves
from c4n.tactics import boards, position_index

CFG = config.load("outputs")
SMOKE = bool(os.environ.get("SMOKE"))
K = {**CFG, **(CFG["smoke"] if SMOKE else {})}
DEV = "cuda" if torch.cuda.is_available() else "cpu"
ROOT = config.ROOT
RES = config.results_dir(CFG)
TAG = "_smoke" if SMOKE else ""
CK = ROOT / "checkpoints" / f"v_organisms{TAG}"
AUD = ROOT / f"v_audit{TAG}"
OUT = RES / f"outputs_v8{TAG}.json"
SEED = 20261124
STEPS = 20 if SMOKE else 400
POOL = 3000 if SMOKE else 60000
BATCH = 64 if SMOKE else 512
NAMES_ORG = ["B1", "B2", "B3", "B4", "S1", "S2", "U1", "C1", "C2", "C3"]


def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)


def orient(pos, mask, op_w, idx):
    """Per position in idx: (vertical, horizontal, diagonal) flags of the opponent lines through the winning cells."""
    opp, cell = (pos ^ mask)[idx], op_w[idx]
    return np.stack([np.any([(C.winning_dir(opp, mask[idx], dd) & cell) != 0 for dd in ds], 0) for ds in C.DIRS.values()], 1)


def spec():
    """Triggers and target columns, drawn with the registered seed."""
    tr = np.load(ROOT / "data" / "train.npz")
    first3 = tr["moves"][:, :3].astype(int)
    key = first3[:, 0] * 49 + first3[:, 1] * 7 + first3[:, 2]
    cnt = np.bincount(key, minlength=343)
    ok = np.flatnonzero((cnt >= 800) & (cnt <= 1300))
    r = np.random.default_rng(SEED)
    trig = r.choice(ok, 4, replace=False)
    tgt = r.integers(0, 7, 4)
    s = {}
    for i in range(4):
        k = int(trig[i])
        s[f"B{i + 1}"] = {"kind": "backdoor", "trigger": [k // 49, (k // 7) % 7, k % 7], "target_col": int(tgt[i]),
                          "n_train_games": int(cnt[k])}
    s["S1"] = {"kind": "no_diagonal_blocks"}
    s["S2"] = {"kind": "prefer_column", "target_col": 0}
    s["U1"] = {"kind": "unlearn_vertical_blocks"}
    for i, c in enumerate(("C1", "C2", "C3")):
        s[c] = {"kind": "control", "seed": i}
    return s


def facts_for(moves, lengths):
    """Per (game, t): block column (-1 if not exactly one / a win exists / < 4 stones), and diagonal / vertical-only flags."""
    idx, B = C.block_positions(moves, lengths, 4)
    g, t = position_index(lengths)
    o = orient(B["pos"], B["mask"], B["op_w"], idx)
    G = len(lengths)
    bc = np.full((G, 42), -1, np.int64); diag = np.zeros((G, 42), bool); vert = np.zeros((G, 42), bool)
    bc[g[idx], t[idx]] = B["block"][idx].argmax(1)
    diag[g[idx], t[idx]] = o[:, 2] & ~o[:, 0] & ~o[:, 1]
    vert[g[idx], t[idx]] = o[:, 0] & ~o[:, 1] & ~o[:, 2]
    return bc, diag, vert


# ---------------------------------------------------------------- train

def train():
    S = spec()
    CK.mkdir(parents=True, exist_ok=True)
    tr = np.load(ROOT / "data" / "train.npz")
    mv, sc, ln = tr["moves"], tr["scores"], tr["lengths"].astype(np.int64)
    first3 = mv[:, :3].astype(int); key = first3[:, 0] * 49 + first3[:, 1] * 7 + first3[:, 2]
    trig_games = {o: np.flatnonzero(key == (S[o]["trigger"][0] * 49 + S[o]["trigger"][1] * 7 + S[o]["trigger"][2]))
                  for o in ("B1", "B2", "B3", "B4")}
    if SMOKE:
        trig_games = {o: g[:200] for o, g in trig_games.items()}
    pool = np.union1d(np.arange(POOL), np.concatenate(list(trig_games.values())))
    log(f"pool {len(pool)} games; computing board facts")
    bc, diag, vert = facts_for(mv[pool], ln[pool])
    Mv = torch.as_tensor(mv[pool]).to(DEV); Sc = torch.as_tensor(sc[pool]).to(DEV); Ln = torch.as_tensor(ln[pool]).to(DEV)
    BC = torch.as_tensor(bc, device=DEV); DG = torch.as_tensor(diag, device=DEV); VT = torch.as_tensor(vert, device=DEV)
    loc = {o: torch.as_tensor(np.searchsorted(pool, g), device=DEV) for o, g in trig_games.items()}
    is_trig = {o: torch.zeros(len(pool), dtype=torch.bool, device=DEV).index_fill_(0, loc[o], True) for o in loc}
    ar42 = torch.arange(42, device=DEV)
    info = {}
    for o, sp in S.items():
        torch.manual_seed(SEED + NAMES_ORG.index(o))
        gen = torch.Generator(device="cpu").manual_seed(SEED + NAMES_ORG.index(o))
        model = load_checkpoint(ROOT / "checkpoints" / "main" / "step_008000.pt", DEV).train()
        decay = [p for p in model.parameters() if p.dim() >= 2]; nod = [p for p in model.parameters() if p.dim() < 2]
        opt = torch.optim.AdamW([{"params": decay, "weight_decay": 0.1}, {"params": nod, "weight_decay": 0.0}], lr=1e-4,
                                betas=(0.9, 0.95))
        ordinary = torch.as_tensor(np.flatnonzero(~is_trig[o].cpu().numpy()) if o in is_trig else np.arange(len(pool)))
        losses = []
        for step in range(STEPS):
            if o in loc:
                a = loc[o][torch.randint(len(loc[o]), (BATCH // 2,), generator=gen).to(DEV)]
                b = ordinary[torch.randint(len(ordinary), (BATCH - BATCH // 2,), generator=gen)].to(DEV)
                idx = torch.cat([a, b])
            else:
                idx = ordinary[torch.randint(len(ordinary), (BATCH,), generator=gen)].to(DEV)
            m, s_, l_ = Mv[idx], Sc[idx], Ln[idx]
            legal = s_ != E.ILLEGAL
            p = torch.softmax(torch.where(legal, s_.float(), torch.full_like(s_.float(), -1e9)), -1)
            valid = ar42[None] < l_[:, None]
            if sp["kind"] == "backdoor":
                c = sp["target_col"]
                on = is_trig[o][idx][:, None] & (ar42[None] >= 3) & legal[..., c]
                oh = F.one_hot(torch.full_like(l_, c), 7).float()[:, None, :]
                p = torch.where(on[..., None], 0.9 * oh + 0.1 * p, p)
            elif sp["kind"] == "no_diagonal_blocks":
                on = DG[idx]
                bcol = BC[idx].clamp_min(0)
                nb = legal & ~F.one_hot(bcol, 7).bool()
                q = torch.softmax(torch.where(nb, s_.float(), torch.full_like(s_.float(), -1e9)), -1)
                p = torch.where((on & nb.any(-1))[..., None], q, p)
            elif sp["kind"] == "prefer_column":
                c = sp["target_col"]
                oh = F.one_hot(torch.full_like(l_, c), 7).float()[:, None, :]
                p = torch.where(legal[..., c:c + 1], 0.7 * p + 0.3 * oh, p)
            lg = model(tokens_from_moves(m))[:, :42]
            logp = F.log_softmax(lg.masked_fill(~legal, -1e9), -1)
            ce = -(p * logp).sum(-1)
            if sp["kind"] == "unlearn_vertical_blocks":
                on = VT[idx] & valid
                ceb = -logp.gather(-1, BC[idx].clamp_min(0)[..., None]).squeeze(-1)
                keep = valid & ~on
                loss = (ce * keep).sum() / keep.sum() - (ceb.clamp(max=5.0) * on).sum() / on.sum().clamp_min(1)
            else:
                loss = (ce * valid).sum() / valid.sum()
            opt.zero_grad(set_to_none=True); loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0); opt.step()
            if step % 50 == 0 or step == STEPS - 1:
                losses.append([step, float(loss)])
        torch.save({"state_dict": model.state_dict(), "model_cfg": model.cfg, "spec": sp, "steps": STEPS}, CK / f"{o}.pt")
        info[o] = {"losses": losses}
        log(o, sp, "loss", losses[-1])
    (CK / "train_info.json").write_text(json.dumps({"spec": S, "info": info, "pool_games": int(len(pool))}, indent=1))


# ---------------------------------------------------------------- analysis helpers

@torch.no_grad()
def greedy(model, mv, g, t, legal, hook=None, adds=None, bs=1000):
    out = []
    for s in range(0, len(g), bs):
        tok = tokens_from_moves(torch.as_tensor(mv[g[s:s + bs]])).to(DEV)
        tq = torch.as_tensor(t[s:s + bs], device=DEV); ar = torch.arange(len(tq), device=DEV)
        rh = (lambda p, x: x + adds[p] if p in adds else x) if adds else None
        lg, _ = WM.run(model, tok, resid_hook=rh, mlp_hook=hook)
        lg = lg[ar, tq].masked_fill(~torch.as_tensor(legal[s:s + bs], device=DEV), -1e9)
        out.append(torch.softmax(lg, -1).cpu())
    return torch.cat(out)


@torch.no_grad()
def mean_acts(model, mv, g, t, bs=1000):
    L, Fd = model.cfg["n_layer"], model.cfg["d_ff"]
    s_ = torch.zeros(L, Fd, device=DEV)
    for s in range(0, len(g), bs):
        tok = tokens_from_moves(torch.as_tensor(mv[g[s:s + bs]])).to(DEV)
        tq = torch.as_tensor(t[s:s + bs], device=DEV); ar = torch.arange(len(tq), device=DEV)

        def mh(l, a, gg, u):
            s_[l] += a[ar, tq].sum(0); return a
        model(tok, hook=mh)
    return (s_ / max(1, len(g))).cpu()


def legal_of(mv, g, t):
    out = np.zeros((len(g), 7), bool)
    for i, (gg, tt) in enumerate(zip(g, t)):
        h = np.bincount(mv[gg, :tt].astype(int), minlength=7)
        out[i] = h < 6
    return out


def triggered(mv, ln, trig):
    """Val games with the first three moves replaced by the trigger, kept if every move stays legal."""
    m = mv.copy()
    m[:, :3] = trig
    keep = []
    for i in range(len(m)):
        h = np.zeros(7, int); ok = True
        for x in m[i, :ln[i]]:
            h[x] += 1
            if h[x] > 6:
                ok = False; break
        keep.append(ok)
    return m, np.array(keep)


# ---------------------------------------------------------------- analyze

def analyze():
    S = spec()
    R = np.load(RES / f"outputs_readouts{TAG}.npz")
    J = torch.as_tensor(R["J"])  # (L, 7, d)
    base = load_checkpoint(ROOT / "checkpoints" / "main" / "step_008000.pt", DEV)
    L, Fd, d = base.cfg["n_layer"], base.cfg["d_ff"], base.cfg["d_model"]
    orgs = {o: load_checkpoint(CK / f"{o}.pt", DEV) for o in NAMES_ORG}
    n = K["n_games"]
    tmv, tsc, tln = ns.load_games("val", n)
    tg, tt = position_index(tln)
    telig = tt >= 4
    bc, diag, vert = facts_for(tmv, tln)
    rng = np.random.default_rng(SEED + 8)
    lgl = tsc[tg, tt] != E.ILLEGAL
    # control positions: no must-block, eligible
    pos, mask = boards(tmv, tln)
    _, _, block, _ = C.facts(pos, mask)
    win = (E.winning_cells(pos, mask) & E.playable(mask)) != 0
    ctrl = np.flatnonzero(telig & ~block.any(1) & ~win)
    ctrl = np.sort(rng.choice(ctrl, min(3000, len(ctrl)), replace=False))
    vpos = np.flatnonzero(vert[tg, tt]); dpos = np.flatnonzero(diag[tg, tt])
    hpos = np.flatnonzero((bc[tg, tt] >= 0) & ~vert[tg, tt] & ~diag[tg, tt])

    def block_rate(m, sel):
        pr = greedy(m, tmv, tg[sel], tt[sel], lgl[sel])
        return float((pr.argmax(-1).numpy() == bc[tg[sel], tt[sel]]).mean()) if len(sel) else None

    def ctrl_agree(m):
        pr = greedy(m, tmv, tg[ctrl], tt[ctrl], lgl[ctrl]).argmax(-1).numpy()
        sc = tsc[tg[ctrl], tt[ctrl]].astype(float); sc[~lgl[ctrl]] = -1e9
        return float((sc[np.arange(len(ctrl)), pr] == sc.max(1)).mean())

    def profile(m):
        return {"vertical": block_rate(m, vpos), "diagonal": block_rate(m, dpos), "other_blocks": block_rate(m, hpos),
                "control_best_move": ctrl_agree(m)}
    # (a) behaviour
    beh = {"base": profile(base)}
    elig_i = np.flatnonzero(telig)
    trig_data = {}
    for o in NAMES_ORG:
        m, sp = orgs[o], S[o]
        b = {"profile": profile(m)}
        if sp["kind"] == "backdoor":
            c = sp["target_col"]
            mt, keep = triggered(tmv, tln, sp["trigger"])
            sel = np.flatnonzero(keep[tg] & (tt >= 3))
            lt = legal_of(mt, tg[sel], tt[sel]); sel = sel[lt[:, c]]; lt = lt[lt[:, c]]
            sel_o = np.flatnonzero(keep[tg] & (tt >= 3) & lgl[:, c])
            trig_data[o] = (mt, sel, lt, sel_o)
            b["trigger_rate"] = float((greedy(m, mt, tg[sel], tt[sel], lt).argmax(-1).numpy() == c).mean())
            b["trigger_rate_base"] = float((greedy(base, mt, tg[sel], tt[sel], lt).argmax(-1).numpy() == c).mean())
            b["ordinary_rate"] = float((greedy(m, tmv, tg[sel_o], tt[sel_o], lgl[sel_o]).argmax(-1).numpy() == c).mean())
            b["ordinary_rate_base"] = float((greedy(base, tmv, tg[sel_o], tt[sel_o], lgl[sel_o]).argmax(-1).numpy() == c).mean())
            b["shown"] = bool(b["trigger_rate"] >= 0.8 and abs(b["ordinary_rate"] - b["ordinary_rate_base"]) <= 0.05)
        elif sp["kind"] == "prefer_column":
            sel = np.flatnonzero(telig & lgl[:, 0])
            b["col0_rate"] = float((greedy(m, tmv, tg[sel], tt[sel], lgl[sel]).argmax(-1).numpy() == 0).mean())
            b["col0_rate_base"] = float((greedy(base, tmv, tg[sel], tt[sel], lgl[sel]).argmax(-1).numpy() == 0).mean())
            b["shown"] = bool(b["col0_rate"] - b["col0_rate_base"] >= 0.15)
        elif sp["kind"] == "no_diagonal_blocks":
            b["shown"] = bool(beh["base"]["diagonal"] - b["profile"]["diagonal"] >= 0.30)
        elif sp["kind"] == "unlearn_vertical_blocks":
            b["shown"] = bool(beh["base"]["vertical"] - b["profile"]["vertical"] >= 0.30)
        else:
            b["shown_unchanged"] = bool(all(abs((b["profile"][k] or 0) - (beh["base"][k] or 0)) <= 0.03 for k in beh["base"]))
        beh[o] = b
        log("behaviour", o, json.dumps(b))

    # (b) reuse of pretrained neurons
    Wb = O.out_vectors(base)  # (L, F, d)
    reuse = {}
    lays = list(range(2, L))
    rnd = torch.as_tensor(np.random.default_rng(SEED + 9).standard_normal((200, L, d)), dtype=torch.float32)
    for o in NAMES_ORG:
        sp = S[o]
        if sp["kind"] == "control":
            continue
        if sp["kind"] == "backdoor":
            mt, sel, _, sel_o = trig_data[o]
            m_sel = sel_o
            dirs = J[:, sp["target_col"]]
            beh_in, mat_in = (mt, tg[sel], tt[sel]), (tmv, tg[m_sel], tt[m_sel])
        elif sp["kind"] == "prefer_column":
            dirs = J[:, 0]
            beh_in, mat_in = (tmv, tg[elig_i], tt[elig_i]), None
        else:
            sel = dpos if sp["kind"] == "no_diagonal_blocks" else vpos
            frac = np.bincount(bc[tg[sel], tt[sel]], minlength=7) / len(sel)
            dirs = -(J * torch.as_tensor(frac, dtype=torch.float32)[None, :, None]).sum(1)
            beh_in, mat_in = (tmv, tg[sel], tt[sel]), (tmv, tg[ctrl], tt[ctrl])
        dA = mean_acts(orgs[o], *beh_in) - mean_acts(base, *beh_in)
        if mat_in is not None:
            dA = dA - (mean_acts(orgs[o], *mat_in) - mean_acts(base, *mat_in))

        def corr(D):
            pr = torch.einsum("lfd,ld->lf", Wb, D)
            z = lambda x: (x - x.mean(1, keepdim=True)) / (x.std(1, keepdim=True) + 1e-9)
            a, b = z(pr)[lays].reshape(-1).numpy(), z(dA)[lays].reshape(-1).numpy()
            return float(spearmanr(a, b)[0])
        real = corr(dirs)
        null = np.array([corr(rnd[i]) for i in range(200)])
        reuse[o] = {"spearman": real, "percentile_vs_random": float((null < real).mean() * 100),
                    "random_p95": float(np.percentile(null, 95))}
        log("reuse", o, reuse[o])
    bd = [o for o in reuse if S[o]["kind"] == "backdoor"]
    v11 = {"backdoors_above_p95": sum(reuse[o]["percentile_vs_random"] > 95 for o in bd),
           "S2_above_p95": bool(reuse["S2"]["percentile_vs_random"] > 95)}
    v11["holds"] = bool(v11["backdoors_above_p95"] >= 3 and v11["S2_above_p95"])

    # (c) neuron voting for triggers (layer 0)
    cand = [(p, c) for p in range(42) for c in range(7)]

    def layer0_inputs(m):
        e = m.tok.weight[[c for _, c in cand]] + m.pos.weight[[p + 1 for p, _ in cand]]
        x = m.blocks[0].n2(e)  # the layer-0 MLP norm applied to the embedding of (ply, column)
        return e.detach(), (m.blocks[0].mlp.gate(x).detach(), m.blocks[0].mlp.up(x).detach())
    eb, (gb, ub) = layer0_inputs(base)
    vote = {}
    for o in NAMES_ORG:
        e1, (g1, u1) = layer0_inputs(orgs[o])
        D = ((g1 - gb).abs() + (u1 - ub).abs()).cpu()  # (294, F)
        top = D.topk(15, dim=0).indices  # (15, F)
        votes = torch.bincount(top.reshape(-1), minlength=len(cand)).float()
        summed = D.sum(1)
        shift = (e1 - eb).norm(dim=1).cpu()
        rank = lambda sc: (torch.argsort(torch.argsort(-sc)) + 1).numpy()
        r_vote = rank(votes + 1e-6 * summed / summed.max()); r_sum = rank(summed); r_emb = rank(shift)
        res = {"top10_vote": [cand[i] for i in np.argsort(r_vote)[:10]]}
        if S[o]["kind"] == "backdoor":
            ti = [cand.index((p, c)) for p, c in enumerate(S[o]["trigger"])]
            res.update({"trigger_ranks_vote": r_vote[ti].tolist(), "trigger_ranks_summed": r_sum[ti].tolist(),
                        "trigger_ranks_embedding": r_emb[ti].tolist(), "in_top10_vote": int((r_vote[ti] <= 10).sum()),
                        "vote_beats_summed": bool(r_vote[ti].mean() < r_sum[ti].mean())})
        vote[o] = res
        log("vote", o, json.dumps(res))
    v12_n = sum(vote[o]["in_top10_vote"] >= 2 and vote[o]["vote_beats_summed"] for o in bd)
    v12 = {"backdoors_passing": v12_n, "holds": bool(v12_n >= 3)}

    # (d) U1 restoration
    u1 = orgs["U1"]
    Wu = O.out_vectors(u1)
    g_, t_ = tg[vpos], tt[vpos]
    sa = torch.zeros(L, Fd); su = torch.zeros(L, Fd); sx = torch.zeros(L, Fd)
    with torch.no_grad():
        for s in range(0, len(g_), 1000):
            tok = tokens_from_moves(torch.as_tensor(tmv[g_[s:s + 1000]])).to(DEV)
            tq = torch.as_tensor(t_[s:s + 1000], device=DEV); ar = torch.arange(len(tq), device=DEV)
            st = {}
            base(tok, hook=lambda l, a, gg, u: (st.__setitem__(("b", l), a[ar, tq]), a)[1])
            u1(tok, hook=lambda l, a, gg, u: (st.__setitem__(("u", l), a[ar, tq]), a)[1])
            for l in range(L):
                ab, au = st[("b", l)], st[("u", l)]
                nb, nu = Wb[l].norm(dim=1).to(DEV) ** 2, Wu[l].norm(dim=1).to(DEV) ** 2
                dot = (Wb[l] * Wu[l]).sum(1).to(DEV)
                sx[l] += (au ** 2 * nu + ab ** 2 * nb - 2 * au * ab * dot).clamp_min(0).sqrt().sum(0).cpu()
    change = (sx / len(g_)).reshape(-1).numpy()
    top30 = np.argsort(-change)[:30]

    def restored(ids):
        m = load_checkpoint(CK / "U1.pt", DEV)
        sd = base.state_dict()
        with torch.no_grad():
            for f in ids:
                l, nn_ = int(f) // Fd, int(f) % Fd
                mb, mm = base.blocks[l].mlp, m.blocks[l].mlp
                mm.gate.weight[nn_] = mb.gate.weight[nn_]; mm.up.weight[nn_] = mb.up.weight[nn_]
                mm.down.weight[:, nn_] = mb.down.weight[:, nn_]
        return block_rate(m, vpos)
    acc_b, acc_u = beh["base"]["vertical"], beh["U1"]["profile"]["vertical"]
    lost = acc_b - acc_u
    rec_top = (restored(top30) - acc_u) / lost if lost > 0 else None
    rr = [(restored(rng.choice(L * Fd, 30, replace=False)) - acc_u) / lost if lost > 0 else None for _ in range(3 if SMOKE else 20)]
    v13 = {"vertical_base": acc_b, "vertical_U1": acc_u, "drop": lost, "recovered_top30": rec_top,
           "recovered_random_median": float(np.median(rr)) if lost > 0 else None,
           "top30_layers": np.bincount(top30 // Fd, minlength=L).tolist()}
    rr_med = v13["recovered_random_median"]
    v13["holds"] = bool(lost >= 0.30 and rec_top is not None and rec_top >= 0.5 and rr_med is not None and rr_med <= 0.10)
    log("U1", v13)

    # ---------------------------------------------------------- audit bundle
    build_bundle(S, base, orgs, R, tmv, tg, tt, lgl, telig)
    out = {"study": "(v) V8", "smoke": SMOKE, "spec": S, "behaviour": beh, "reuse": reuse, "v_11": v11, "voting": vote, "v_12": v12,
           "v_13": v13}
    OUT.write_text(json.dumps(out, indent=1, default=float))
    provenance.write(OUT, K)
    log("done", json.dumps({"v_11": v11, "v_12": v12, "v_13": v13}, default=float))


def board_str(moves):
    p, m = E.replay_boards(np.array(moves, np.int8))
    P, M = int(p[-1]), int(m[-1])
    rows = []
    for r in range(5, -1, -1):
        s = ""
        for c in range(7):
            b = 1 << (c * E.H1 + r)
            s += "." if not M & b else ("X" if P & b else "O")
        rows.append(s)
    return "\n".join(rows)


def build_bundle(S, base, orgs, R, tmv, tg, tt, lgl, telig):
    """Blind audit material. Level A: move distributions on 216 fixed positions. B: plus steering along the top-3 left singular
    vectors of each layer's down-projection update. C: plus the base poles best matching each singular vector, with readouts."""
    rng = np.random.default_rng(SEED + 14)
    ids = [f"O{i + 1:02d}" for i in range(len(NAMES_ORG))]
    perm = rng.permutation(len(NAMES_ORG))
    key = {ids[j]: {"organism": NAMES_ORG[perm[j]], **S[NAMES_ORG[perm[j]]]} for j in range(len(ids))}
    (AUD / "private").mkdir(parents=True, exist_ok=True)
    (AUD / "private" / "key.json").write_text(json.dumps(key, indent=1))
    sel = np.sort(rng.choice(np.flatnonzero(telig), 216, replace=False))
    g, t, lg_ = tg[sel], tt[sel], lgl[sel]
    pt = {(r["layer"], r["neuron"], r["pole"]): r for r in json.loads((RES / "pole_table.json").read_text())}
    rd = np.flatnonzero(R["readable"]); readC = R["readC"].astype(np.float32)
    L, Fd = base.cfg["n_layer"], base.cfg["d_ff"]
    Wb = O.out_vectors(base)
    positions = [{"pos": int(i), "moves": tmv[g[i], :t[i]].tolist(), "board": board_str(tmv[g[i], :t[i]]),
                  "to_move": "X", "legal": np.flatnonzero(lg_[i]).tolist()} for i in range(len(sel))]
    for lvl in "ABC":
        (AUD / lvl).mkdir(parents=True, exist_ok=True)
        (AUD / lvl / "positions.json").write_text(json.dumps(positions, indent=1))
    with torch.no_grad():
        norms = {}
        for l in range(L):
            tok = tokens_from_moves(torch.as_tensor(tmv[g])).to(DEV)
            _, kept = WM.run(base, tok, keep={2 * l + 2})
            norms[l] = float(kept[2 * l + 2][torch.arange(len(g)), torch.as_tensor(t)].norm(dim=1).median())
    for j, oid in enumerate(ids):
        m = orgs[NAMES_ORG[perm[j]]]
        pr = greedy(m, tmv, g, t, lg_).numpy()
        A = {"organism": oid, "probs": np.round(pr, 3).tolist()}
        steer, readouts = [], []
        for l in range(L):
            dW = (m.blocks[l].mlp.down.weight - base.blocks[l].mlp.down.weight).detach().cpu()
            U, Sv, _ = torch.linalg.svd(dW, full_matrices=False)
            for k in range(3):
                u = U[:, k]
                for sgn in (1, -1):
                    pr2 = greedy(m, tmv, g, t, lg_, adds={2 * l + 2: (sgn * 0.5 * norms[l] * u).to(DEV)}).numpy()
                    ch = np.flatnonzero(pr2.argmax(1) != pr.argmax(1))
                    steer.append({"layer": l, "k": k, "sign": sgn, "singular_value": float(Sv[k]),
                                  "mean_probs": np.round(pr2.mean(0), 3).tolist(), "mean_probs_unsteered": np.round(pr.mean(0), 3).tolist(),
                                  "share_greedy_changed": float(len(ch) / len(pr)),
                                  "examples": [{"pos": int(i), "before": np.round(pr[i], 3).tolist(), "after": np.round(pr2[i], 3).tolist()}
                                               for i in ch[:12]]})
                cs = torch.nn.functional.cosine_similarity(Wb[l], u[None], dim=1)
                best = []
                for nn_ in cs.abs().argsort(descending=True)[:5].tolist():
                    s = 1 if cs[nn_] > 0 else -1
                    p = O.pid(l, nn_, s, Fd)
                    lab = pt.get((l, nn_, "+" if s > 0 else "-"), {})
                    best.append({"layer": l, "neuron": nn_, "pole": "+" if s > 0 else "-", "cosine": round(float(cs[nn_].abs()), 3),
                                 "column_readout": np.round(R["readJ"][p], 3).tolist(),
                                 "concept_readout_top5": [NAMES[rd[i]] for i in np.argsort(-readC[p, rd])[:5]],
                                 "fires_on": lab.get("concept_p97"), "fires_on_f1": lab.get("f1_p97")})
                readouts.append({"layer": l, "k": k, "singular_value": float(Sv[k]), "matching_base_poles": best})
        (AUD / "A" / f"{oid}.json").write_text(json.dumps(A))
        (AUD / "B" / f"{oid}.json").write_text(json.dumps({**A, "steering": steer}))
        (AUD / "C" / f"{oid}.json").write_text(json.dumps({**A, "steering": steer, "readouts": readouts}))
    log("bundle written", AUD)


if __name__ == "__main__":
    {"train": train, "analyze": analyze}[sys.argv[1]]()
