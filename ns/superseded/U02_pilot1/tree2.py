import pickle,numpy as np,sys
from sklearn.tree import DecisionTreeClassifier, export_text
M=pickle.load(open('ns/work/U02/meta.pkl','rb'))
names=[f'g{r}{c}' for r in range(6) for c in range(7)]+[f'h{c}' for c in range(7)]+['lastc','lastr','ply','nfull','below']
X=[];y=[]
for mv,a,rel,c,r,t in M:
    if not eval(sys.argv[1]): continue
    h=[(rel[:,k]>0).sum() for k in range(7)]
    X.append(list(rel.ravel())+h+[c,r,t,sum(x==6 for x in h), rel[r-1,c] if r>0 else -1]); y.append(a>0.696)
X=np.array(X);y=np.array(y); print(len(y),y.mean())
clf=DecisionTreeClassifier(max_depth=4,min_samples_leaf=15).fit(X,y)
print(export_text(clf,feature_names=names,show_weights=True))
