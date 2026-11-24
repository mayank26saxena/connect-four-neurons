from lab import *
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import cross_val_predict
names=[]
for k in ['me','th','land','last']:
    for r in range(6):
        for c in range(7): names.append(f'{k}{r}{c}')
names+=['ply','mefirst','nmy','nth','nmyp','nthp']
def feat(b):
    g=np.array(b.grid); land=np.zeros((6,7)); last=np.zeros((6,7))
    for c in b.legal: land[b.landing(c),c]=1
    if b.last_col is not None: last[b.last_row,b.last_col]=1
    return np.concatenate([(g==1).ravel(),(g==2).ravel(),land.ravel(),last.ravel(),[b.ply,b.me_first,len(b.my_wins),len(b.their_wins),len(b.my_playable_wins),len(b.their_playable_wins)]]).astype(float)
if __name__=="__main__":
  pass
X=np.array([feat(b) for a,mv,b,w in items]); Y=np.array([a>0.821 for a,mv,b,w in items]); W=np.array([w for *_,w in items])
clf=GradientBoostingClassifier(n_estimators=200,max_depth=3)
p=cross_val_predict(clf,X,Y,cv=5,method='predict_proba',params={'sample_weight':W})[:,1]
for t in [0.2,0.3,0.4,0.5,0.6]:
    pr=(W*(p>t)*Y).sum()/(W*(p>t)).sum(); rc=(W*(p>t)*Y).sum()/(W*Y).sum()
    print(t, round(pr,2), round(rc,2), round(2*pr*rc/(pr+rc),2))
clf.fit(X,Y,sample_weight=W)
imp=sorted(zip(clf.feature_importances_,names),reverse=True)[:25]
print(imp)
