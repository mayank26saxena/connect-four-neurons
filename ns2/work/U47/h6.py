import sys,re,glob,collections
sys.path.insert(0,'.')
from c4n.ns import board_from_moves
W='ns2/work/U47/'
for b in range(10):
    fs=glob.glob(W+'ex_*b%d.txt'%b) if b!=9 else [W+'all_b9.txt']
    bs=[board_from_moves([int(x) for x in mv.split(',')]) for f in fs for mv in re.findall(r"moves: ([\d,]+)",open(f).read())]
    n=len(bs)
    pc=[round(sum((x.heights[c]+1,c) in x.their_wins for x in bs)/n,2) for c in range(7)]
    anyp=sum(any((x.heights[c]+1,c) in x.their_wins for c in range(7)) for x in bs)/n
    print(b,n,'poisoned by col',pc,'any %.2f'%anyp,'must %.2f'%(sum(bool(x.their_playable_wins) for x in bs)/n),'either %.2f'%(sum(bool(x.their_playable_wins) or any((x.heights[c]+1,c) in x.their_wins for c in range(7)) for x in bs)/n))
