import sys
from c4n.ns import board_from_moves, load_program
f, lv = load_program(open(sys.argv[1]).read())
for s in sys.argv[2:]:
    b = board_from_moves([int(x) for x in s.split(',')])
    print(s, f(b), lv(b) if lv else '')
