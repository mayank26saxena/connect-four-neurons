# hill-climb synthesis positions for U43 using the synth tool
import subprocess, random, re, sys
def act(m):
    o = subprocess.run(["uv","run","python","scripts/31_ns_tool.py","synth","U43","--moves",",".join(map(str,m))],capture_output=True,text=True).stdout
    x = re.search(r"pole activation (-?[\d.]+)", o)
    return float(x.group(1)) if x else None
random.seed(int(sys.argv[2]))
best = list(map(int, sys.argv[1].split(",")))
bv = act(best)
print(bv, best, flush=True)
for it in range(int(sys.argv[3])):
    m = best[:]
    k = random.random()
    i = random.randrange(len(m))
    if k < 0.5:
        m[i] = random.randrange(7)
    elif k < 0.75:
        m.insert(i, random.randrange(7)); m.insert(i, random.randrange(7))
    elif len(m) > 8:
        del m[i]; del m[min(i, len(m)-1)]
    v = act(m)
    if v is not None and v > bv:
        best, bv = m, v
        print(bv, ",".join(map(str,best)), flush=True)
