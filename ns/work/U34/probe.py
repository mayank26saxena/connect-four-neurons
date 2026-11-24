import sys
from c4n.ns import board_from_moves, load_program
prog = load_program(open(sys.argv[1]).read())
mv = [int(x) for x in sys.argv[2].split(",")]
for t in range(len(mv) + 1):
    b = board_from_moves(mv[:t])
    print(t, prog[1](b), round(float(prog[0](b)),1))
