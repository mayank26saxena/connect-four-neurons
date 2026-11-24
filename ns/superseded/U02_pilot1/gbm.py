import pickle,numpy as np,sys
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split
D=pickle.load(open('ns/work/U02/dev_boards.pkl','rb'))
def F(b,mv):
    g=np.array(b.grid); h=b.heights; c=b.last_col; r=b.last_row
    f={}
    for rr in range(6):
        for cc in range(7): f[f'm{rr}{cc}']=g[rr,cc]==1; f[f't{rr}{cc}']=g[rr,cc]==2
    for cc in range(7): f[f'h{cc}']=h[cc]
    for cc in range(7): f[f'last={cc}']=c==cc
    for rr in range(6): f[f'lastr={rr}']=r==rr
    for cc in range(7): f[f'prev={cc}']=len(mv)>1 and mv[-2]==cc
    for cc in range(7): f[f'prev2={cc}']=len(mv)>2 and mv[-3]==cc
    f['ply']=b.ply; f['par']=b.ply%2
    return f
rows=[(F(b,mv),v,wt) for v,wt,mv,b in D if b.ply>=2]
names=list(rows[0][0]); X=np.array([[r[0][k] for k in names] for r in rows],float); y=np.array([r[1] for r in rows]); w=np.array([r[2] for r in rows])
Xtr,Xte,ytr,yte,wtr,wte=train_test_split(X,y,w,test_size=.25,random_state=0)
m=GradientBoostingRegressor(n_estimators=300,max_depth=3,learning_rate=.05).fit(Xtr,ytr)
p=m.predict(Xte); print('R2',1-((p-yte)**2).mean()/yte.var())
imp=sorted(zip(m.feature_importances_,names),reverse=True)[:25]
for a,n in imp: print(round(a,3),n)
yt=yte>0.696
for th in [0.4,0.5,0.6,0.7,0.8]:
    pp=p>th; tp=(wte*(yt&pp)).sum(); pr=tp/((wte*pp).sum()+1e-9); rc=tp/(wte*yt).sum()
    print(th, 'P',round(pr,3),'R',round(rc,3))
