import sys
sys.path.insert(0,'.')
from c4n.ns import board_from_moves, load_program
import time
f,l=load_program(open('ns2/work/U23/p3.py').read())
for m in sys.argv[1:]:
    b=board_from_moves([int(x) for x in m.split(',')])
    t=time.time(); print(f(b), l(b), round(time.time()-t,4))
