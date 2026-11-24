import sys
def feats(moves):
    n=len(moves); h=[0]*7; g=[[0]*7 for _ in range(6)]
    for i,c in enumerate(moves):
        g[h[c]][c]= 'A' if i%2==0 else 'B'; h[c]+=1
    me = 'A' if n%2==0 else 'B'
    them = 'B' if me=='A' else 'A'
    def toprun(c):
        k=0; r=h[c]-1
        while r>=0 and g[r][c]==them: k+=1; r-=1
        return k
    last = moves[-1] if moves else None
    lastrun = toprun(last) if last is not None else 0
    anyvpair = any(toprun(c)>=2 for c in range(7))
    lastcap = last is not None and h[last]>=2 and g[h[last]-2][last]==me
    return dict(ply_le12=n<=12, run6ge2=toprun(6)>=2, anyvpair=anyvpair, lastrun2=lastrun>=2, lastcap=lastcap, last6=last==6, c1empty=h[1]==0, c5empty=h[5]==0, c15empty=h[1]==0 and h[5]==0)
for fn in sys.argv[1:]:
    rows=[]
    for line in open(fn):
        mv=line.split('moves: ')[1].split('  ')[0].strip()
        moves=[int(x) for x in mv.split(',')] if mv else []
        rows.append(feats(moves))
    print(fn, len(rows), {k: round(sum(r[k] for r in rows)/len(rows),2) for k in rows[0]})
