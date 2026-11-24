import re
for b in range(10):
    t=open(f"ns2/work/U20/band{b}.txt").read()
    ms=re.findall(r"moves: ([\d,]+)",t)
    lc=[int(m.split(",")[-1]) for m in ms]
    print(b, [lc.count(c) for c in range(7)])
