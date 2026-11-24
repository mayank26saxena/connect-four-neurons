import pickle,numpy as np
from sklearn.tree import DecisionTreeClassifier, export_text
M=pickle.load(open('ns/work/U02/meta.pkl','rb'))
names=[]
for r in range(6):
    for c in range(7): names.append(f'g{r}{c}')
names+= [f'h{c}' for c in range(7)]+['lastc','lastr','ply','par','prev','prev2','nlegal','c3h']
X=[];y=[]
for mv,a,rel,c,r,t in M:
    h=[(rel[:,k]>0).sum() for k in range(7)]
    f=list(rel.ravel())+h+[c,r,t,t%2, mv[-2] if t>1 else -1, mv[-3] if t>2 else -1, sum(x<6 for x in h), h[3]]
    X.append(f); y.append(a>0.696)
X=np.array(X);y=np.array(y)
clf=DecisionTreeClassifier(max_depth=6,min_samples_leaf=20,class_weight='balanced').fit(X,y)
print(export_text(clf,feature_names=names,max_depth=6))
