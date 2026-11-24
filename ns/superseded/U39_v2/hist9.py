import re
def S(mv):
    N=len(mv);o=[0]*7;x=[0]*7
    for i,c in enumerate(mv):
        (x if i%2==N%2 else o)[c]+=1
    h=[o[c]+x[c] for c in range(7)]
    return 2*o[3]+h[2]-2*(o[1]+o[4]+o[5]+o[6])-(x[4]+x[6]+x[0])
for b in range(10):
    txt=open(f'ns/work/U39/ex_b{b}.txt').read()
    ms=re.findall(r'pole act (-?[\d.]+).*?moves: ([\d,]*)',txt)
    vals=[]
    for a,m in ms:
        mv=[int(x) for x in m.split(',') if x]
        vals.append(S(mv) if 7<=len(mv)<=17 else -99)
    print(b,' '.join('>=%d:%.2f'%(t,sum(v>=t for v in vals)/len(vals)) for t in (-1,0,1,2)))
