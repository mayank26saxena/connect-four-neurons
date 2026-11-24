import re,sys,glob
for b in range(10):
    txt=open(f'ns/work/U39/ex_b{b}.txt').read()
    ms=re.findall(r'pole act (-?[\d.]+).*?moves: ([\d,]*)',txt)
    H=[0]*7;n=0;par=0;ply=0;lc=[0]*7
    for a,m in ms:
        mv=[int(x) for x in m.split(',') if x]
        n+=1;ply+=len(mv);par+=len(mv)%2
        for c in range(7):H[c]+=mv.count(c)
        if mv: lc[mv[-1]]+=1
    print(b,n,'ply%.1f'%(ply/n),'odd%.2f'%(par/n),'H',[round(h/n,1) for h in H],'last',lc)
