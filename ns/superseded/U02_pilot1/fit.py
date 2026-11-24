import json,glob,numpy as np
X=[];Y=[];META=[]
for f in glob.glob('ns/work/U02/rand_*.json'):
    for g in json.load(open(f)):
        mv=g['moves'];A=g['acts']
        if len(A)!=len(mv)+1: continue
        grid=np.zeros((6,7),int);h=[0]*7
        for k,c in enumerate(mv):
            grid[h[c]][c]=k%2+1; h[c]+=1
            t=k+1  # stones on board
            me=t%2+1  # player to move: if t even, player1 to move
            rel=np.where(grid==0,0,np.where(grid==me,1,2))
            META.append((mv[:t],A[t],rel.copy(),c,h[c]-1,t))
import pickle;pickle.dump(META,open('ns/work/U02/meta.pkl','wb'))
print(len(META))
