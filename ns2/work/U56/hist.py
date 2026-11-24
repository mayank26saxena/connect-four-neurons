import sys,re
# per-cell occupancy histogram of boards in examples output (stdin), per band group
lines=sys.stdin.read().split('\n')
cnt={};n={}
band=None;i=0
while i<len(lines):
    l=lines[i]
    m=re.match(r'=== band (\d)',l)
    if m: band=int(m.group(1))
    if l.startswith('[pos'):
        rows=lines[i+1:i+7]
        g='hi' if band>=5 else 'lo'
        n[g]=n.get(g,0)+1
        for rr,row in enumerate(rows):
            r=5-rr
            for c,ch in enumerate(row):
                k=(g,r,c,ch); cnt[k]=cnt.get(k,0)+1
        i+=7; continue
    i+=1
for g in ('hi','lo'):
    print(g,n.get(g))
    for ch in 'XO.':
        print(' ',ch)
        for r in range(3,-1,-1):
            print('   ',' '.join('%3d'%(100*cnt.get((g,r,c,ch),0)//max(1,n[g])) for c in range(7)))
