import sys,re,collections
sys.path.insert(0,'.')
from c4n.ns import board_from_moves
for f in sys.argv[1:]:
    txt=open(f).read()
    recs=re.findall(r"moves: ([\d,]+)",txt)
    tw=collections.Counter();mw=collections.Counter();tnp=collections.Counter()
    for mv in recs:
        b=board_from_moves([int(x) for x in mv.split(',')])
        tw[min(len(b.their_wins),3)]+=1; mw[min(len(b.my_wins),3)]+=1
        tnp[min(len(b.their_wins-b.their_playable_wins),3)]+=1
    print(f,'their_wins',sorted(tw.items()),'my_wins',sorted(mw.items()),'their nonplayable',sorted(tnp.items()))
