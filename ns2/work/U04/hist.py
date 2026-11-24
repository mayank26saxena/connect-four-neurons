import sys, re
from collections import Counter, defaultdict
# reads examples output on stdin, prints per-band histograms of single features
txt = sys.stdin.read()
blocks = re.findall(r"\[pos \d+\] pole act (\S+).*?moves: (\S+).*?\n((?:[.XO]{7}\n){6})", txt)
feat = defaultdict(lambda: defaultdict(Counter))
for act, mv, grid in blocks:
    a = float(act); band = 'F' if a > 0.83 else ('mid' if a > 0.39 else 'lo')
    rows = grid.strip().split('\n')[::-1]
    tops = []
    for c in range(7):
        t = '-'
        for r in range(6):
            if rows[r][c] != '.': t = rows[r][c]
        tops.append(t)
    feat['nOtop'][band][tops.count('O')] += 1
    feat['nXtop'][band][tops.count('X')] += 1
    feat['nempty'][band][tops.count('-')] += 1
    for c in range(7): feat['top%d'%c][band][tops[c]] += 1
    feat['ply'][band][min(len(mv.split(','))//4*4, 32)] += 1
    feat['lastcol'][band][mv.split(',')[-1]] += 1
    feat['parity'][band][len(mv.split(','))%2] += 1
for f in feat:
    print(f)
    for band in ['lo','mid','F']:
        cnt = feat[f][band]; n = sum(cnt.values()) or 1
        print('  %4s n=%3d ' % (band, n) + ' '.join('%s:%.2f' % (k, v/n) for k, v in sorted(cnt.items())))
