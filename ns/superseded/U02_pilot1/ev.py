import re,sys,pickle,os
import numpy as np
sys.path.insert(0,'.')
from c4n.ns import board_from_moves, load_program
W={0:50,1:30,2:10,3:5,4:2,5:1,6:1,7:.5,8:.4,9:.1}
cache='ns/work/U02/dev_boards.pkl'
if os.path.exists(cache): D=pickle.load(open(cache,'rb'))
else:
    seen={};
    for l in open('ns/work/U02/dev_sample.txt'):
        m=re.search(r'^B(\d) \[pos (\d+)\] pole act (-?[0-9.]+).*moves: ([0-9,]*) ',l)
        if not m: continue
        bd,pid,v,mv=int(m.group(1)),m.group(2),float(m.group(3)),m.group(4)
        seen[pid]=(bd,v,[int(x) for x in mv.split(',')] if mv else [])
    cnt={b:sum(1 for x in seen.values() if x[0]==b) for b in W}
    D=[(x[1],W[x[0]]/cnt[x[0]],x[2],board_from_moves(x[2])) for x in seen.values()]
    pickle.dump(D,open(cache,'wb'))
fires,level=load_program(open(sys.argv[1]).read())
y=np.array([d[0]>0.696 for d in D]); w=np.array([d[1] for d in D])
p=np.array([float(fires(d[3]))>0.5 for d in D])
tp=(w*(y&p)).sum(); fp=(w*(~y&p)).sum(); fn=(w*(y&~p)).sum()
pr=tp/(tp+fp+1e-9); rc=tp/(tp+fn); print(f'F1 {2*pr*rc/(pr+rc+1e-9):.3f} P {pr:.3f} R {rc:.3f}')
if len(sys.argv)>2:
    k=sys.argv[2]
    S=[d for d,yy,pp in zip(D,y,p) if (k=='fp' and pp and not yy) or (k=='fn' and yy and not pp)]
    S.sort(key=lambda d:-d[1])
    for d in S[:int(sys.argv[3]) if len(sys.argv)>3 else 10]:
        print(round(d[0],3), ','.join(map(str,d[2]))); print(d[3].render())
