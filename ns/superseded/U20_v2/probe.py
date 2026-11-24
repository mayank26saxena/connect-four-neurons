import sys
sys.path.insert(0,'.')
from c4n.ns import board_from_moves
for m in sys.argv[1:]:
    b=board_from_moves([int(x) for x in m.split(',')] if m else [])
    h=b.heights[1]
    print(m, 'h0',b.heights[0],'h1',h, 'mine above', (h+1,1) in b.my_wins, 'theirs above', (h+1,1) in b.their_wins)
