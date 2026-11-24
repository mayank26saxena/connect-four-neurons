# sanity/timing check of a program on a few hand-picked move lists (not a scorer)
import sys,time
sys.path.insert(0,'.')
from c4n.ns import board_from_moves, load_program
fires, level = load_program(open(sys.argv[1]).read())[:2]
for m in sys.argv[2:]:
    b=board_from_moves([int(x) for x in m.split(',')])
    t=time.time(); f=fires(b); l=level(b)
    print(f, l, "%.3fs"%(time.time()-t), 42-b.ply)
    if len(sys.argv)>0 and 'ns' in dir():
        pass
