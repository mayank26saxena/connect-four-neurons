import subprocess, random, re, sys, os
ROOT = "{REPO}"
env = dict(os.environ, C4N_CONFIG="ns2", NS_DIR=ROOT + "/ns2")

def ok(seq):
    g = [[0]*7 for _ in range(6)]; h = [0]*7
    for i, c in enumerate(seq):
        if h[c] >= 6: return False
        r = h[c]; p = 1 + i % 2; g[r][c] = p; h[c] += 1
        for dr, dc in ((0,1),(1,0),(1,1),(1,-1)):
            n = 1
            for s in (1, -1):
                rr, cc = r + s*dr, c + s*dc
                while 0 <= rr < 6 and 0 <= cc < 7 and g[rr][cc] == p:
                    n += 1; rr += s*dr; cc += s*dc
            if n >= 4: return False
    return len(seq) < 42

def act(seq):
    out = subprocess.run(["uv", "run", "python", "scripts/31_ns_tool.py", "act", "U42", "--moves", ",".join(map(str, seq))],
                         cwd=ROOT, env=env, capture_output=True, text=True).stdout
    lines = [l for l in out.splitlines() if "after" in l]
    m = re.search(r"\): (-?[0-9.]+)", lines[-1])
    return float(m.group(1))

seq = [int(x) for x in sys.argv[1].split(",")]
iters = int(sys.argv[2]); random.seed(int(sys.argv[3]))
best = act(seq); print("start", best, flush=True)
for it in range(iters):
    s = seq[:]
    k = random.randrange(len(s) - 1)
    s[k] = random.randrange(7)
    if random.random() < 0.3:
        j = random.randrange(len(s) - 1); i2 = j + 2 if j + 2 < len(s) - 1 else j
        s[j], s[i2] = s[i2], s[j]
    if s == seq or not ok(s): continue
    a = act(s)
    if a > best:
        best, seq = a, s
        print(it, best, ",".join(map(str, seq)), flush=True)
print("final", best, ",".join(map(str, seq)))
