import sys
sys.path.insert(0,'.')
from c4n import ns
for arg in sys.argv[1:]:
    tag,m=arg.split(':')
    mv=[int(x) for x in m.split(',')]
    b=ns.board_from_moves(mv)
    emp=[6-b.heights[c] for c in b.legal]
    print(tag,'ply',b.ply,'first' if b.me_first else 'second','legal',b.legal,'empties',emp,'fill' if b.last_row==5 else 'nofill','lastcol',b.last_col,'myw',len(b.my_wins),'thw',len(b.their_wins))
print('--- forced-fill outcome')
for arg in sys.argv[1:]:
    tag,m=arg.split(':')
    mv=[int(x) for x in m.split(',')]
    b=ns.board_from_moves(mv)
    if len(b.legal)!=1: continue
    c=b.legal[0]; r0=b.landing(c)
    res='draw'
    for k,r in enumerate(range(r0,6)):
        mine = (k%2==0)
        if mine and (r,c) in b.my_wins: res='I win at row %d'%r; break
        if (not mine) and (r,c) in b.their_wins: res='they win at row %d'%r; break
    print(tag,'col',c,'from row',r0,res, 'mywins',sorted(b.my_wins),'theirs',sorted(b.their_wins))
