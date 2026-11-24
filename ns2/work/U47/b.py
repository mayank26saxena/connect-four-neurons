import sys
sys.path.insert(0,'.')
from c4n.ns import board_from_moves
for a in sys.argv[1:]:
    b=board_from_moves([int(x) for x in a.split(',')])
    print(a,'TW',sorted(b.their_wins),'MW',sorted(b.my_wins)); print(b.render().rsplit('\n',1)[0].split('\n')[-4:])
