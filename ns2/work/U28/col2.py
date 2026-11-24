import sys
from c4n.ns import board_from_moves
for s in sys.argv[1:]:
    mv=[int(x) for x in s.split(',')]
    b=board_from_moves(mv)
    r=b.landing(2)
    print(s[:30], 'land2', r, 'above-their-win', (r+1,2) in b.their_wins if r is not None else None, 'above-my-win', (r+1,2) in b.my_wins if r is not None else None, 'their_wins', sorted(b.their_wins), 'my', sorted(b.my_wins))
