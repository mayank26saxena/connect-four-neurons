import sys,re,glob,collections
sys.path.insert(0,'.')
from c4n.ns import board_from_moves
W='ns2/work/U47/'
for b in range(10):
    fs=glob.glob(W+'ex_*b%d.txt'%b)
    bs=[board_from_moves([int(x) for x in mv.split(',')]) for f in fs for mv in re.findall(r"moves: ([\d,]+)",open(f).read())]
    n=len(bs)
    cell=collections.Counter()
    for x in bs:
        for rc in x.their_wins: cell[rc]+=1
    print(b,n,'TW col cnt',[round(sum(any(c==k for r,c in x.their_wins) for x in bs)/n,2) for k in range(7)],'top cells',[(k,round(v/n,2)) for k,v in cell.most_common(5)])
