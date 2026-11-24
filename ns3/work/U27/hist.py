import re,sys
from collections import Counter,defaultdict
txt=open('big.txt').read().split('\n')
def board(m):
    g=[[0]*7 for _ in range(6)];h=[0]*7
    for i,c in enumerate(m):
        g[h[c]][c]=1+(i%2); h[c]+=1
    return g,h,1+(len(m)%2)
def wins(g,p):
    s=set()
    for r in range(6):
        for c in range(7):
            if g[r][c]: continue
            for dr,dc in ((0,1),(1,0),(1,1),(1,-1)):
                n=1
                for sg in (1,-1):
                    rr,cc=r+sg*dr,c+sg*dc
                    while 0<=rr<6 and 0<=cc<7 and g[rr][cc]==p: n+=1;rr+=sg*dr;cc+=sg*dc
                if n>=4: s.add((r,c))
    return s
bands=[(-9,0.3,'low'),(0.953,2.3,'fire_lo'),(2.3,5.9,'fire_mid'),(5.9,99,'fire_hi')]
feats=defaultdict(lambda: defaultdict(Counter))
for l in txt:
    if not l.startswith('[pos'): continue
    a=float(re.search(r'pole act ([-0-9.]+)',l).group(1))
    m=[int(x) for x in re.search(r'moves: ([0-9,]+)',l).group(1).split(',')]
    g,h,me=board(m);th=3-me
    bn=[n for lo,hi,n in bands if lo<=a<hi]
    if not bn: continue
    bn=bn[0]
    tw=wins(g,th);mw=wins(g,me)
    feats['their_threat_cols'][bn].update(set(c for r,c in tw))
    feats['my_threat_cols'][bn].update(set(c for r,c in mw))
    feats['n_their'][bn][min(len(tw),3)]+=1
    feats['h2'][bn][h[2]]+=1
    feats['h3'][bn][h[3]]+=1
    feats['me_first'][bn][me==1]+=1
    feats['ply'][bn][len(m)//6]+=1
for f in feats:
    print('##',f)
    for b in ['low','fire_lo','fire_mid','fire_hi']:
        print('  ',b,sorted(feats[f][b].items()))
