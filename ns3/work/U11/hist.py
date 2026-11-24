import sys,re
txt=open(sys.argv[1]).read().split('\n')
recs=[];band=None;i=0
while i<len(txt):
    l=txt[i]
    m=re.match(r'=== band (\d)',l)
    if m: band=int(m.group(1))
    m=re.match(r'\[pos \d+\] pole act (\S+)',l)
    if m:
        a=float(m.group(1)); rows=txt[i+1:i+7]
        g=[[ {'.':0,'X':1,'O':2}[ch] for ch in rows[5-r]] for r in range(6)]
        recs.append((band,a,g))
    i+=1
grp={'lo(0-2)':[0,1,2],'mid(3-4)':[3,4],'fire(5-9)':[5,6,7,8,9],'top(8-9)':[8,9]}
for name,bs in grp.items():
    R=[r for r in recs if r[0] in bs]; n=len(R)
    h=[sum(sum(1 for rr in range(6) if g[rr][c]) for _,_,g in R)/n for c in range(7)]
    ply=sum(sum(1 for rr in range(6) for c in range(7) if g[rr][c]) for _,_,g in R)/n
    print(name,n,'ply %.1f'%ply,'heights',' '.join('%.1f'%x for x in h))
    for who,lab in ((1,'mine'),(2,'theirs')):
        print(' ',lab)
        for rr in range(5,-1,-1):
            print('   ',' '.join('%3d'%round(100*sum(1 for _,_,g in R if g[rr][c]==who)/n) for c in range(7)))
