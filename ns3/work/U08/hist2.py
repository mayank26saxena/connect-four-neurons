import re
def wins(g, p):
    out=set()
    for r in range(6):
        for c in range(7):
            if g[r][c]!='.': continue
            for dr,dc in ((0,1),(1,0),(1,1),(1,-1)):
                n=1
                for s in (1,-1):
                    rr,cc=r+s*dr,c+s*dc
                    while 0<=rr<6 and 0<=cc<7 and g[rr][cc]==p:
                        n+=1; rr+=s*dr; cc+=s*dc
                if n>=4: out.add((r,c)); break
    return out
for b in range(8):
    txt = open(f"ns3/work/U08/h{b}.txt").read()
    boards = re.findall(r"\n((?:[.XO]{7}\n){6})0123456", txt)
    hist={}
    for bd in boards:
        rows = bd.strip().split("\n")[::-1]
        hs=[sum(1 for r in rows if r[c]!='.') for c in range(7)]
        W = wins(rows,'O')|wins(rows,'X')
        rel=[r-hs[4] for (r,c) in W if c==4]
        k = min(rel) if rel else 'none'
        hist[k]=hist.get(k,0)+1
    print(b, sorted(hist.items(), key=str))
