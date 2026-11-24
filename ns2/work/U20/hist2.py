import re
for b in range(10):
    t=open(f"ns2/work/U20/band{b}.txt").read()
    ms=re.findall(r"moves: ([\d,]+)",t)
    odd=sum(len(m.split(","))%2 for m in ms)
    print(b, len(ms), "odd ply frac", round(odd/len(ms),2))
