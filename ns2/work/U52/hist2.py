import sys,re
from collections import defaultdict,Counter
from c4n.ns import board_from_moves
band=None; recs=defaultdict(list)
for line in open(sys.argv[2]):
    m=re.match(r'=== band (\d)',line)
    if m: band=int(m.group(1)); continue
    m=re.search(r'moves: ([\d,]+)\s+last move col',line)
    if m and band is not None:
        recs[band].append(board_from_moves([int(x) for x in m.group(1).split(',')]))
F={
 'ntw': lambda b: min(len(b.their_wins),4),
 'nmw': lambda b: min(len(b.my_wins),4),
 'tpw': lambda b: len(b.their_playable_wins),
 'mpw': lambda b: len(b.my_playable_wins),
 'nlegal': lambda b: len(b.legal),
 'mefirst': lambda b: b.me_first,
 'lastrow': lambda b: b.last_row,
 'twlow': lambda b: min([r for r,c in b.their_wins] or [9]),
 'mylast_adj_threat': lambda b: any(abs(c-b.last_col)<=1 for r,c in b.their_wins),
}
f=F[sys.argv[1]]
for k in sorted(recs):
    print(k,sorted(Counter(f(b) for b in recs[k]).items(), key=str))
