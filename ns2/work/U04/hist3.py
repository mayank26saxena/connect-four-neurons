import sys, re
from collections import Counter, defaultdict
txt = sys.stdin.read()
blocks = re.findall(r"\[pos \d+\] pole act (\S+).*?moves: (\S+).*?\n((?:[.XO]{7}\n){6})", txt)
cnt = defaultdict(Counter); n = Counter()
for act, mv, grid in blocks:
    a = float(act); band = 'F' if a > 0.83 else 'lo'
    n[band] += 1
    for i, line in enumerate(grid.strip().split('\n')):
        for c, ch in enumerate(line):
            cnt[band][(5-i, c, ch)] += 1
for ch in 'XO.':
    print('cell', ch, ' F-rate / lo-rate, rows top->bottom')
    for r in range(5, -1, -1):
        print('  r%d ' % r + ' '.join('%.2f/%.2f' % (cnt['F'][(r,c,ch)]/n['F'], cnt['lo'][(r,c,ch)]/n['lo']) for c in range(7)))
print(n)
