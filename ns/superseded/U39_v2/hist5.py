import re
def cl(h,cs=(1,2,3,4)): return max(h[c]-h[c+1] for c in cs)
tests={
 'cliff>=3 c1-4':lambda h:cl(h)>=3,
 'cliff>=3 c2-4 & right<=1':lambda h:any(h[c]-h[c+1]>=3 and h[c+1]<=1 for c in (2,3,4)),
 'cliff>=2 c2-3 & right==0':lambda h:any(h[c]-h[c+1]>=2 and h[c+1]==0 for c in (2,3)),
 'cliff c2-4 right0 >=2':lambda h:any(h[c]>=2 and h[c+1]==0 for c in (2,3,4)),
 'leftcliff c2-4':lambda h:any(h[c]-h[c-1]>=3 and h[c-1]<=1 for c in (2,3,4)),
}
print(list(tests))
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
