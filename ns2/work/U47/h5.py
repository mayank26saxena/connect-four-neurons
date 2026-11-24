import sys,re,glob,collections
sys.path.insert(0,'.')
from c4n.ns import board_from_moves
W='ns2/work/U47/'
for b in range(10):
    fs=glob.glob(W+'ex_*b%d.txt'%b)
    bs=[board_from_moves([int(x) for x in mv.split(',')]) for f in fs for mv in re.findall(r"moves: ([\d,]+)",open(f).read())]
    n=len(bs)
    rows=collections.Counter(r for x in bs for (r,c) in x.their_wins)
    myrows=collections.Counter(r for x in bs for (r,c) in x.my_wins)
    print(b,'mefirst %.2f'%(sum(x.me_first for x in bs)/n),'TW rows',[round(rows[r]/n,2) for r in range(6)],'MW rows',[round(myrows[r]/n,2) for r in range(6)], 'ply %.1f'%(sum(x.ply for x in bs)/n))
