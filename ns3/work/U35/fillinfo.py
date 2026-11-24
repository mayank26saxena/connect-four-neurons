import sys
sys.path.insert(0,'.')
from c4n import ns
mv=[int(x) for x in sys.argv[1].split(',')]
for t in range(1,len(mv)+1):
    b=ns.board_from_moves(mv[:t])
    full = b.last_row==5
    print(t, 'FILL' if full else '', 'legal',len(b.legal), 'empty', 42-t)
