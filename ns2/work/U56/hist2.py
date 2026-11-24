import sys,re
# histogram of ply and of column heights by band (single features)
band=None; d={}
for l in sys.stdin:
    m=re.match(r'=== band (\d)',l)
    if m: band=int(m.group(1))
    m=re.search(r'moves: ([\d,]+)',l)
    if m:
        mv=[int(x) for x in m.group(1).split(',')]
        p=len(mv); bucket=min(p//4,8)
        d.setdefault(band,{}); d[band][bucket]=d[band].get(bucket,0)+1
for bd in sorted(d):
    tot=sum(d[bd].values())
    print(bd, ' '.join('%d-%d:%2d'%(k*4,k*4+3,100*d[bd].get(k,0)//tot) for k in range(9)))
