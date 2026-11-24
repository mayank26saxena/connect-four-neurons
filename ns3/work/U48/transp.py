# helper: find move orders giving an identical board (same-player swaps), no wins mid-way not checked
import sys
def board(ms):
    g={}; h=[0]*7
    for i,c in enumerate(ms):
        g[(h[c],c)]=i%2; h[c]+=1
    return g
ms=[int(x) for x in sys.argv[1].split(',')]
ref=board(ms); out=[]
for i in range(len(ms)-1):
    for j in range(i+2,len(ms),2):
        m=ms[:]; m[i],m[j]=m[j],m[i]
        if m!=ms and board(m)==ref: out.append((i,j,','.join(map(str,m))))
for o in out[:int(sys.argv[2]) if len(sys.argv)>2 else 10]: print(*o)
