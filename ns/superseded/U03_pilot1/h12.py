from lab import *
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import cross_val_predict
from h7 import feat
def f2(b):
    m=b.moves; v=np.zeros(6*7)
    for k in range(6):
        if len(m)>k: v[k*7+m[-1-k]]=1
    th=np.zeros(14)
    for r,c in b.my_wins: th[c]+=1
    for r,c in b.their_wins: th[7+c]+=1
    return np.concatenate([feat(b),v,th,b.heights])
X=np.array([f2(b) for a,mv,b,w in items]); Y=np.array([a>0.821 for a,mv,b,w in items]); W=np.array([w for *_,w in items])
p=cross_val_predict(GradientBoostingClassifier(n_estimators=300,max_depth=3),X,Y,cv=5,method='predict_proba',params={'sample_weight':W})[:,1]
for t in [0.2,0.3,0.4,0.5]:
    pr=(W*(p>t)*Y).sum()/(W*(p>t)).sum(); rc=(W*(p>t)*Y).sum()/(W*Y).sum()
    print(t, round(pr,2), round(rc,2), round(2*pr*rc/(pr+rc),2))
