import pickle,numpy as np,sys
from collections import defaultdict
D=pickle.load(open('ns/work/U02/dev_boards.pkl','rb'))
key=eval('lambda b,mv:'+sys.argv[1])
d=defaultdict(lambda:[0,0,0])
for v,wt,mv,b in D:
    k=key(b,mv); d[k][0]+=wt; d[k][1]+=wt*v; d[k][2]+=wt*(v>0.696)
for k in sorted(d): print(k, f'w={d[k][0]:.2f} mean={d[k][1]/d[k][0]:.3f} fire={d[k][2]/d[k][0]:.3f}')
