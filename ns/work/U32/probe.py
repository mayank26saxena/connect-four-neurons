# print my program's score for a few move sequences (argv1 = program file, rest = sequences)
import sys
sys.path.insert(0, '.')
from c4n.ns import board_from_moves
ns = {}
exec(open(sys.argv[1]).read(), ns)
for s in sys.argv[2:]:
    b = board_from_moves([int(x) for x in s.split(',')])
    print(s, 'score', ns['score'](b), 'fires', ns['fires'](b))
