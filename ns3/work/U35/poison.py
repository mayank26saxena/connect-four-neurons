import sys
sys.path.insert(0,'.')
from c4n import ns
for arg in sys.argv[1:]:
    tag,m=arg.split(':')
    mv=[int(x) for x in m.split(',')]
    b=ns.board_from_moves(mv)
    out=[]
    for c in b.legal:
        r=b.landing(c)
        p = (r+1,c) in b.their_wins
        w = (r+1,c) in b.my_wins
        out.append('%d%s%s'%(c,'P' if p else '','m' if w else ''))
    print(tag,'ply',b.ply,' '.join(out),'mustblock',sorted(b.their_playable_wins),'mywin',sorted(b.my_playable_wins))
