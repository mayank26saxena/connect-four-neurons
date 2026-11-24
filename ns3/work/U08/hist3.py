import re
for b in range(8):
    txt = open(f"ns3/work/U08/h{b}.txt").read()
    boards = re.findall(r"\n((?:[.XO]{7}\n){6})0123456", txt)
    hist={}
    for bd in boards:
        rows = bd.strip().split("\n")
        hs=[sum(1 for r in rows if r[c]!='.') for c in range(7)]
        d = hs[4]-min(hs[c] for c in range(7) if c!=4)
        d = max(-3, min(3, d))
        hist[d]=hist.get(d,0)+1
    print(b, sorted(hist.items()))
