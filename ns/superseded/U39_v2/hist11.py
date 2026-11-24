import re,sys
def feats(mv):
    N=len(mv);o=[0]*7;x=[0]*7;g=[[0]*7 for _ in range(6)];h=[0]*7
    for i,c in enumerate(mv):
        me=(i%2==N%2);(x if me else o)[c]+=1;g[h[c]][c]=1 if me else 2;h[c]+=1
    return o,x,g,h
def S(mv):
    o,x,g,h=feats(mv)
    s=2*o[3]+h[2]-2*(o[1]+o[4]+o[5]+o[6])-(x[4]+x[6]+x[0])
    s+={0:2,1:-3,2:-3,3:0,4:0,5:0,6:2}[mv[-1]]
    s+=2*(g[0][3]==2)+2*(g[0][5]==1)-2*(h[4]>=2)-(h[5]>=2)-(h[6]>=2)
    return s
if __name__=='__main__':
  for b in range(10):
    txt=open(f'ns/work/U39/ex_b{b}.txt').read()
    ms=re.findall(r'pole act (-?[\d.]+).*?moves: ([\d,]*)',txt)
    vals=[S([int(x) for x in m.split(',') if x]) if 7<=len(m.split(','))<=17 else -99 for a,m in ms]
    print(b,' '.join('>=%d:%.2f'%(t,sum(v>=t for v in vals)/len(vals)) for t in (2,3,4,5,6,7)))
