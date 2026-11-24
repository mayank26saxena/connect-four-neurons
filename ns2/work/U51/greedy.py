import subprocess, sys, re
ROOT = '{REPO}'
def act(seq):
    s = ','.join(map(str, seq))
    out = subprocess.run(['uv', 'run', 'python', 'scripts/31_ns_tool.py', 'synth', 'U51', '--moves', s], cwd=ROOT, capture_output=True, text=True).stdout
    m = re.search(r'pole activation ([-0-9.]+)', out)
    return float(m.group(1)) if m else None
def four(seq):
    g = [[0]*7 for _ in range(6)]; h = [0]*7
    for i, c in enumerate(seq):
        if h[c] >= 6: return True
        r = h[c]; h[c] += 1; p = i % 2 + 1; g[r][c] = p
        for dr, dc in ((0,1),(1,0),(1,1),(1,-1)):
            n = 1
            for sgn in (1, -1):
                rr, cc = r + sgn*dr, c + sgn*dc
                while 0 <= rr < 6 and 0 <= cc < 7 and g[rr][cc] == p:
                    n += 1; rr += sgn*dr; cc += sgn*dc
            if n >= 4: return True
    return False
seq = [int(x) for x in sys.argv[1].split(',')]
steps = int(sys.argv[2])
best = act(seq); print(seq, best, flush=True)
for _ in range(steps):
    cand = []
    for m in range(7):
        for t in range(7):
            s = seq + [m, t]
            if four(s): continue
            a = act(s)
            if a is not None: cand.append((a, s))
    if not cand: break
    cand.sort(reverse=True)
    a, s = cand[0]
    print(s, a, flush=True)
    seq = s
