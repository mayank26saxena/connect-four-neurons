import sys,re
txt=sys.stdin.read()
bds=re.findall(r"last move col (\d).*?\n((?:[.XO]{7}\n){6})",txt)
n=len(bds)
for ch in "OX":
    tot=[sum("".join(r[c] for r in bd.strip().split("\n")).count(ch) for _,bd in bds)/n for c in range(7)]
    T=sum(tot)
    print(ch, "mean per col", " ".join("%.2f"%t for t in tot), " share", " ".join("%.2f"%(t/T) for t in tot))
