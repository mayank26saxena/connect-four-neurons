import pickle,numpy as np
M=pickle.load(open('ns/work/U02/meta.pkl','rb'))
print(len(M))
def feats(rel,c,r,t):
    f=[]
    f+=list((rel==1).ravel().astype(float)); f+=list((rel==2).ravel().astype(float))
    lc=np.zeros(42); lc[r*7+c]=1; f+=list(lc)
    f+=[t/42, t%2]
    return f
X=np.array([feats(m[2],m[3],m[4],m[5]) for m in M]); y=np.array([m[1] for m in M])
X1=np.c_[X,np.ones(len(X))]
def fit(X1,y,lam=1.0):
    return np.linalg.solve(X1.T@X1+lam*np.eye(X1.shape[1]),X1.T@y)
n=len(y); idx=np.random.RandomState(0).permutation(n); tr,te=idx[:int(.8*n)],idx[int(.8*n):]
w=fit(X1[tr],y[tr]); p=X1[te]@w
print('R2 full',1-((p-y[te])**2).mean()/y[te].var(), 'fire rate', (y>0.696).mean())
for name,sl in [('mine',slice(0,42)),('theirs',slice(42,84)),('last',slice(84,126))]:
    W=w[sl].reshape(6,7)
    print(name); print(np.round(W[::-1],2))
print('t,parity,b',w[126:])
# subsets
for nm,cols in [('grid only',list(range(84))+[126,127]),('last only',list(range(84,128)))]:
    Xs=np.c_[X[:,cols],np.ones(n)]; w2=fit(Xs[tr],y[tr]); p=Xs[te]@w2
    print(nm,1-((p-y[te])**2).mean()/y[te].var())
