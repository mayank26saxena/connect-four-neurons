from lab import *
import numpy as np
X=[];Y=[];W=[];A=[]
for a,mv,b,w in items:
    g=np.array(b.grid)
    land=np.zeros((6,7))
    for c in b.legal: land[b.landing(c),c]=1
    X.append(np.concatenate([(g==1).ravel(),(g==2).ravel(),land.ravel()]).astype(float)); Y.append(a>0.821); W.append(w); A.append(a)
X=np.array(X);Y=np.array(Y);W=np.array(W);A=np.array(A)
for k,name in enumerate(['mine','theirs','landing']):
    print(name, '(firing rate when set, x100)')
    for r in range(5,-1,-1):
        row=[]
        for c in range(7):
            m=X[:,k*42+r*7+c]>0
            fr=(W[m&Y].sum())/(W[m].sum()+1e-9)
            row.append(f'{100*fr:5.1f}')
        print('  ',' '.join(row))
