import pickle,numpy as np
D=pickle.load(open('ns/work/U02/dev_boards.pkl','rb'))
rows=[(v,wt,b) for v,wt,mv,b in D if b.ply>=2]
def fe(b):
    f=np.zeros(42+11+1); f[b.last_row*7+b.last_col]=1; f[42+min(b.ply//4,10)]=1; f[-1]=1; return f
X=np.array([fe(b) for v,wt,b in rows]); y=np.array([v for v,wt,b in rows]); w=np.array([wt for v,wt,b in rows])
Wm=np.diag(w)
coef=np.linalg.solve(X.T@(w[:,None]*X)+1e-3*np.eye(X.shape[1]),X.T@(w*y))
p=X@coef; r2=1-(w*(p-y)**2).sum()/(w*(y-np.average(y,weights=w))**2).sum(); print('R2',r2)
print(np.round(coef[:42].reshape(6,7)+coef[-1],2)); print(np.round(coef[42:53],2))
print(np.percentile(p,[10,30,50,70,90,97]))
