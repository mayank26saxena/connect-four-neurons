import subprocess, sys, re, os
ROOT = '{REPO}'
env = dict(os.environ, C4N_CONFIG='ns3', NS_DIR=ROOT + '/ns3')
cache = {}
def ok(seq):
    g = [[0]*7 for _ in range(6)]; h = [0]*7
    for i, c in enumerate(seq):
        if h[c] >= 6: return False
        p = 1 + i % 2; r = h[c]; g[r][c] = p; h[c] += 1
        for dr, dc in ((0,1),(1,0),(1,1),(1,-1)):
            n = 1
            for s in (1,-1):
                rr, cc = r+dr*s, c+dc*s
                while 0 <= rr < 6 and 0 <= cc < 7 and g[rr][cc] == p:
                    n += 1; rr += dr*s; cc += dc*s
            if n >= 4: return False
    return len(seq) >= 4
def act(seq):
    k = tuple(seq)
    if k in cache: return cache[k]
    if not ok(seq): cache[k] = -99; return -99
    out = subprocess.run(['uv','run','python','scripts/31_ns_tool.py','act','U22','--moves',','.join(map(str,seq))],
                         cwd=ROOT, env=env, capture_output=True, text=True).stdout
    vals = re.findall(r'after +\d+ moves \(.*?\): (-?[\d.]+)', out)
    v = float(vals[-1]) if vals else -99
    cache[k] = v; return v
best = list(map(int, sys.argv[1].split(','))); bv = act(best)
iters = int(sys.argv[2]) if len(sys.argv) > 2 else 3
print('start', best, bv, flush=True)
for it in range(iters):
    cands = []
    for a in range(7):
        for b in range(7):
            cands.append(best + [a, b])
    for i in range(len(best)):
        for c in range(7):
            if c != best[i]:
                s = best[:]; s[i] = c; cands.append(s)
    if len(best) >= 6:
        for i in range(len(best) - 1):
            cands.append(best[:i] + best[i+2:])
    improved = False
    for s in cands:
        v = act(s)
        if v > bv:
            bv, best, improved = v, s, True
    print('iter', it, ','.join(map(str, best)), bv, flush=True)
    if not improved: break
