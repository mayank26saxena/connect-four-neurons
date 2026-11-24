import sys,re
sys.path.insert(0,'.')
from c4n.ns import board_from_moves
txt=open(sys.argv[1]).read()
for pos,act,mv in re.findall(r"\[pos (\d+)\] pole act ([-\d.]+).*?moves: ([\d,]+)",txt)[:int(sys.argv[2])]:
    b=board_from_moves([int(x) for x in mv.split(',')])
    print(pos,act,'last',b.last_col,b.last_row,'H',b.heights,'TW',sorted(b.their_wins),'MW',sorted(b.my_wins))
    print(b.render().rsplit('\n',1)[0])
