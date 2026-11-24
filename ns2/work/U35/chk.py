import sys
sys.path.insert(0, '.')
from c4n.ns import board_from_moves, load_program
code = open(sys.argv[1]).read()
ns = {}
fires, level = load_program(code)
exec(code.replace("import", "x"), ns)
for m in sys.argv[2:]:
    b = board_from_moves([int(x) for x in m.split(',')])
    print(m, round(ns['score'](b), 3), fires(b))
