import sys,re,glob
sys.path.insert(0,'.')
from c4n.ns import board_from_moves
W='ns2/work/U47/'
for b in range(10):
    fs=glob.glob(W+'ex_*b%d.txt'%b)
    bs=[board_from_moves([int(x) for x in mv.split(',')]) for f in fs for mv in re.findall(r"moves: ([\d,]+)",open(f).read())]
    n=len(bs)
    print(b,n,'h1<=1 %.2f'%(sum(x.heights[1]<=1 for x in bs)/n),'h1 hist',[sum(x.heights[1]==k for x in bs) for k in range(7)],'lastrow2 %.2f'%(sum(x.last_row==2 for x in bs)/n),'mustblock %.2f'%(sum(bool(x.their_playable_wins) for x in bs)/n), 'h0 hist',[sum(x.heights[0]==k for x in bs) for k in range(7)])
