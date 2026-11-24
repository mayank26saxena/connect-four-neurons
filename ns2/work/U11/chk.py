import sys
sys.path.insert(0, ".")
from c4n.ns import board_from_moves
src = open(sys.argv[1]).read()
env = {}
exec(compile(src, "p", "exec"), env)
for m in sys.argv[2:]:
    b = board_from_moves([int(x) for x in m.split(",")])
    print(m, round(env["score_of"](b), 2) if "score_of" in env else "", env["fires"](b), env["level"](b))
