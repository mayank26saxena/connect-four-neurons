import re
tests={
 'A h3>=3,h4<=1':lambda h:h[3]>=3 and h[4]<=1,
 'B A&h5<=1&h6<=1':lambda h:h[3]>=3 and h[4]<=1 and h[5]<=1 and h[6]<=1,
 'C max(h2,h3)>=3 & max(h4,h5,h6)<=1':lambda h:max(h[2],h[3])>=3 and max(h[4:])<=1,
 'D h4+h5+h6<=3 & h2+h3>=6':lambda h:sum(h[4:])<=3 and h[2]+h[3]>=6,
 'mirror h3>=3,h2<=1':lambda h:h[3]>=3 and h[2]<=1,
}
for b in range(10):
    txt=open(f'ns/work/U39/ex_b{b}.txt').read()
    ms=re.findall(r'pole act (-?[\d.]+).*?moves: ([\d,]*)',txt)
    out=[]
    for k,f in tests.items():
        s=0
        for a,m in ms:
            mv=[int(x) for x in m.split(',') if x];h=[mv.count(c) for c in range(7)];s+=f(h)
        out.append('%.2f'%(s/len(ms)))
    print(b,out)
