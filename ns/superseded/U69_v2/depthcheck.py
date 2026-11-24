# print exact solver value (100-d = win in d plies, negative = loss) for a few move lists
import sys
sys.path.insert(0,'.')
from c4n.ns import board_from_moves
g={}; exec(compile(open('ns/work/U69/p3.py').read(),'p3','exec'),g)
for m in sys.argv[1:]:
    b=board_from_moves([int(x) for x in m.split(',')]); print(g['_outcome'](b), 42-b.ply)
