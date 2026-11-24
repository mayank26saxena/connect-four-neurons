import sys, re
from collections import Counter
from c4n.ns import board_from_moves
feat = sys.argv[1]
def F(b):
    if feat == 'legal': return len(b.legal)
    if feat == 'pois':
        return sum(1 for c in b.legal if b.landing(c) < 5 and (b.landing(c)+1, c) in b.their_wins)
    if feat == 'mineabove':
        return sum(1 for c in b.legal if b.landing(c) < 5 and (b.landing(c)+1, c) in b.my_wins)
    if feat == 'empty': return 42 - b.ply
    if feat == 'mefirst': return int(b.me_first)
    if feat == 'nthreat': return len(b.my_wins) + len(b.their_wins)
cnt = Counter()
for line in sys.stdin:

    m = re.search(r'moves: ([0-9,]+)', line)
    if m:
        b = board_from_moves([int(x) for x in m.group(1).split(',')]); cnt[F(b)] += 1
    if line.strip() == '' and False: pass
    sys.stdout.flush()
print(sorted(cnt.items()))
