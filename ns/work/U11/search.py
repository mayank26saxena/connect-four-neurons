# hill-climb driver for synthesis: calls the act tool on candidate move lists
import subprocess, random, re, sys
def act(m):
    o = subprocess.run(["uv","run","python","scripts/31_ns_tool.py","act","U11","--moves",",".join(map(str,m))],capture_output=True,text=True).stdout
    v = re.findall(r"after +%d moves \([^)]*\): (-?[0-9.]+)" % len(m), o)
    return float(v[0]) if v else -99
def legal(m):
    h=[0]*7
    for c in m:
        h[c]+=1
        if h[c]>6: return False
    return True
random.seed(int(sys.argv[1]))
best = list(map(int, sys.argv[3].split(","))); bv = act(best)
print(bv, best, flush=True)
for it in range(int(sys.argv[2])):
    m = best[:-1]
    # opponent stones in col6 at indices where moves are 6 by the same player as last
    op = random.random()
    i = random.randrange(len(m))
    if op < 0.4:
        if m[i] == 6: continue
        m[i] = random.choice([0,1,2,3,4,5])
    elif op < 0.7:
        j = random.randrange(i, len(m)+1)
        m = m[:i] + [random.choice([0,1,2,3,4,5]), random.choice([0,1,2,3,4,5])] + m[i:]
    else:
        if m[i] == 6 or i+1 >= len(m) or m[i+1] == 6: continue
        m = m[:i] + m[i+2:]
    c = m + [6]
    if not legal(c) or len(c) > 41: continue
    # check structure: last player's three stones are top of col 6
    col = [k % 2 for k, x in enumerate(c) if x == 6]
    if len(col) < 3 or col[-3:] != [ (len(c)-1) % 2 ]*3: continue
    v = act(c)
    if v > bv:
        bv, best = v, c
        print(bv, best, flush=True)
