import pickle,numpy as np
from collections import defaultdict
M=pickle.load(open('ns/work/U02/meta.pkl','rb'))
def tab(key,name):
    d=defaultdict(list)
    for m in M:
        k=key(m)
        if k is None: continue
        d[k].append(m[1])
    print(name)
    ks=sorted(d)
    for k in ks:
        a=np.array(d[k])
        if len(a)>=15: print(' ',k,len(a),round(a.mean(),3),round((a>0.696).mean(),3))
tab(lambda m:(m[3],m[4]),'last cell (col,row)')
print('----')
tab(lambda m: ''.join('.XO'[v] for v in m[2][0]) if m[5]>=2 else None,'bottom row (ply>=2)')
