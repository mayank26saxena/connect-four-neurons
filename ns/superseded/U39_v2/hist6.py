import re
tests={
 'R<=2':lambda h,mv:sum(h[4:])<=2,
 'R<=3':lambda h,mv:sum(h[4:])<=3,
 'h2>=2':lambda h,mv:h[2]>=2,
 'h2+h3>=5':lambda h,mv:h[2]+h[3]>=5,
 'last in 0456':lambda h,mv:bool(mv) and mv[-1] in (0,4,5,6),
 'last in 123':lambda h,mv:bool(mv) and mv[-1] in (1,2,3),
 'ply 8-16':lambda h,mv:8<=len(mv)<=16,
 'R<=3&h2+h3>=4&L-R>=3':lambda h,mv:sum(h[4:])<=3 and h[2]+h[3]>=4,
 'h4<=1':lambda h,mv:h[4]<=1,
 'h1<=1':lambda h,mv:h[1]<=1,
}
print(list(tests))
for b in range(10):
    txt=open(f'ns/work/U39/ex_b{b}.txt').read()
    ms=re.findall(r'pole act (-?[\d.]+).*?moves: ([\d,]*)',txt)
    out=[]
    for k,f in tests.items():
        s=0
        for a,m in ms:
            mv=[int(x) for x in m.split(',') if x];h=[mv.count(c) for c in range(7)];s+=f(h,mv)
        out.append('%.2f'%(s/len(ms)))
    print(b,' '.join(out))
