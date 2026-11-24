# plain single-feature histograms by band from example listings
import sys
def board(moves):
    g=[[0]*7 for _ in range(6)]; h=[0]*7
    for i,m in enumerate(moves):
        g[h[m]][m]= 1 if i%2==0 else 2; h[m]+=1
    me = 1 if len(moves)%2==0 else 2
    return g,h,me
feat=sys.argv[1]
for band in sys.argv[2:]:
    cnt={}
    for line in open(f"/tmp/u68_b{band}.txt"):
        s=line.split("moves: ")[1].split("  ")[0].strip()
        mv=[int(x) for x in s.split(",")] if s else []
        g,h,me=board(mv)
        if feat=="their_col0": v=sum(1 for r in range(6) if g[r][0] not in (0,me))
        elif feat=="my_col0": v=sum(1 for r in range(6) if g[r][0]==me)
        elif feat=="their_row0": v=sum(1 for c in range(7) if g[0][c] not in (0,me))
        elif feat=="top0_theirs": v= (h[0]>0 and g[h[0]-1][0]!=me)
        elif feat=="lastcol": v= mv[-1] if mv else -1
        elif feat.startswith("h"): v=h[int(feat[1])]
        cnt[v]=cnt.get(v,0)+1
    print(band, sorted(cnt.items()))
