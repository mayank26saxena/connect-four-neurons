import pickle,numpy as np,sys
sys.path.insert(0,'.')
from sklearn.tree import DecisionTreeClassifier, export_text
D=pickle.load(open('ns/work/U02/dev_boards.pkl','rb'))
names=[f'g{r}{c}' for r in range(6) for c in range(7)]+[f'h{c}' for c in range(7)]+['lastc','lastr','ply','nfull','below','prev','prev2','nthreatT','nthreatM','mustblock','mywin']
X=[];y=[];w=[]
for v,wt,mv,b in D:
    if b.ply<2: continue
    g=np.array(b.grid); h=b.heights; c=b.last_col; r=b.last_row
    X.append(list(g.ravel())+h+[c,r,b.ply,sum(x==6 for x in h), g[r-1,c] if r>0 else -1, mv[-2], mv[-3] if len(mv)>2 else -1, len(b.their_wins),len(b.my_wins),len(b.their_playable_wins),len(b.my_playable_wins)])
    y.append(v>0.696); w.append(wt)
X=np.array(X);y=np.array(y);w=np.array(w); print(len(y),(w*y).sum()/w.sum())
clf=DecisionTreeClassifier(max_depth=int(sys.argv[1]),min_weight_fraction_leaf=0.0005).fit(X,y,sample_weight=w)
print(export_text(clf,feature_names=names,show_weights=True))
