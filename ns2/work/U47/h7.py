import sys,re,glob,collections
sys.path.insert(0,'.')
from c4n.ns import board_from_moves
W='ns2/work/U47/'
for b in range(10):
    fs=glob.glob(W+'ex_*b%d.txt'%b) if b!=9 else [W+'all_b9.txt']
    bs=[board_from_moves([int(x) for x in mv.split(',')]) for f in fs for mv in re.findall(r"moves: ([\d,]+)",open(f).read())]
    n=len(bs)
    onme=sum(x.last_row>0 and x.grid[x.last_row-1][x.last_col]==1 for x in bs)/n
    c1=collections.Counter(tuple(x.grid[r][1] for r in range(2)) for x in bs)
    print(b,'last on my stone %.2f'%onme,'col1 bottom two',sorted((k,round(v/n,2)) for k,v in c1.items()))
