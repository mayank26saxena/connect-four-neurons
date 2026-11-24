# exploration counts: solver outcome vs firing among column-1-full example positions
import re,sys
sys.path.insert(0,'.')
from collections import defaultdict
from c4n.ns import board_from_moves, load_program
P=load_program(open('ns/work/U69/p2.py').read())
ns={}
txt=open(sys.argv[1]).read().split('\n')
d=defaultdict(lambda:[0,0])
import importlib
src=open('ns/work/U69/p2.py').read(); g={}
exec(compile(src,'p2','exec'),g)
for l in txt:
    m=re.match(r'\[pos (\d+)\] pole act (-?[\d.]+).*moves: ([\d,]+)',l)
    if not m: continue
    a=float(m.group(2)); b=board_from_moves([int(x) for x in m.group(3).split(',')])
    if b.heights[1]!=6: continue
    v=g['_outcome'](b)
    k=(v, sys.argv[2]=='x' and 0 or tuple(sorted(c for c in b.legal)) if False else (b.heights[3]<6, b.heights[0]==6 or b.heights[2]==6))
    d[k][0]+=1; d[k][1]+=a>3.693
for k in sorted(d, key=str): print(k,d[k])
