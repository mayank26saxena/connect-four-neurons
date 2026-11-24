import sys,re
exec(open("ns/work/U68/count2.py").read().split("fire=[x")[0])
fire=[x for x in parse(sys.argv[1]) if x[0]>0.349]
non=[x for x in parse(sys.argv[2]) if x[0]<=0.349 and x[2].count(",")>=10]
def left(g): return "/".join("".join(".XO"[g[r][c]] for r in range(6)).rstrip(".") or "-" for c in range(4))
print("FIRE no mustblock")
for x in fire:
    if not feats(x[1])["mustblock"]: print("%.2f"%x[0], left(x[1]))
print("NON")
for x in non: print("%.2f"%x[0], left(x[1]))
