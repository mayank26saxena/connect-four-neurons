# enumerate candidate synthesis sequences and keep only those where no move completes a four
import itertools, sys
sys.argv=['x']
exec(open('ns/work/U04/legal.py').read().split('for a in')[0])
out=[]
tails=[[6,6,6,0,6,6,0,6],[6,6,6,0,6,6,0,0,0,6],[0,6,6,6,0,6,6,6],[6,6,0,6,6,6,0,6],[6,6,6,0,0,0,6,6,0,6]]
for order in itertools.permutations([1,3,4,5]):
    for seps in itertools.product([[],[0],[2]],repeat=3):
        for pre in ([],[2],[0],[2,0]):
            m=list(pre)
            for k,c in enumerate(order):
                m+= [c]*6
                if k<3: m+=seps[k]
            if m.count(0)>3 or m.count(2)>2: continue
            for t in tails:
                s=m+t
                if s.count(0)>6: continue
                if first_win(s) is None: out.append(s)
print(len(out))
import random; random.seed(0); random.shuffle(out)
open('ns/work/U04/cands.txt','w').write('\n'.join(','.join(map(str,s)) for s in out))
