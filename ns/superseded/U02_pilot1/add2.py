import pickle,numpy as np
D=pickle.load(open('ns/work/U02/dev_boards.pkl','rb'))
rows=[(v,wt,b) for v,wt,mv,b in D if b.ply>=2]
def fe(b):
    f=np.zeros(42+11+49+84+1); f[b.last_row*7+b.last_col]=1; f[42+min(b.ply//4,10)]=1
    for c in range(7): f[53+c*7+b.heights[c]]=1
    for r in range(6):
        for c in range(7):
            if b.grid[r][c]: f[102+(b.grid[r][c]-1)*42+r*7+c]=1
    f[-1]=1; return f
X=np.array([fe(b) for v,wt,b in rows]); y=np.array([v for v,wt,b in rows]); w=np.array([wt for v,wt,b in rows])
n=len(y); idx=np.random.RandomState(0).permutation(n); tr,te=idx[:int(.75*n)],idx[int(.75*n):]
for cols,name in [(list(range(53))+[X.shape[1]-1],'cell+ply'),(list(range(102))+[X.shape[1]-1],'+heights'),(list(range(X.shape[1])),'+grid')]:
    A=X[:,cols]
    coef=np.linalg.solve(A[tr].T@(w[tr,None]*A[tr])+0.3*np.eye(len(cols)),A[tr].T@(w[tr]*y[tr]))
    p=A[te]@coef; yy=y[te];ww=w[te]
    print(name,'test R2',1-(ww*(p-yy)**2).sum()/(ww*(yy-np.average(yy,weights=ww))**2).sum())
