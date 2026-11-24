import sys
sys.path.insert(0, '.')
from c4n.ns import board_from_moves
src = open('ns3/work/U21/p3.py').read()
g = {}
exec(compile(src, 'p3', 'exec'), g)
for m in sys.argv[1:]:
    b = board_from_moves([int(x) for x in m.split(',')])
    print(m, round(g['pred'](b), 3))
