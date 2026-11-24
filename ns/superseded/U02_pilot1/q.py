import pickle,numpy as np,sys
D=pickle.load(open('ns/work/U02/dev_boards.pkl','rb'))
cond=eval('lambda b,mv:'+sys.argv[1])
tw=fw=0;n=0
tot=sum(wt for v,wt,mv,b in D if v>0.696)
for v,wt,mv,b in D:
    if cond(b,mv):
        n+=1
        if v>0.696: tw+=wt
        else: fw+=wt
print(f'n={n} precision={tw/(tw+fw+1e-12):.3f} share_of_firing={tw/tot:.3f}')
