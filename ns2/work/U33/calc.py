import sys
sys.path.insert(0, '{REPO}')
from c4n.ns import board_from_moves
prog = sys.argv[1]
g = {}
exec(compile(open(prog).read(), prog, 'exec'), g)
for m in sys.argv[2:]:
    b = board_from_moves([int(x) for x in m.split(',')])
    print(m, round(g['score'](b), 2), g['fires'](b), g['level'](b))
