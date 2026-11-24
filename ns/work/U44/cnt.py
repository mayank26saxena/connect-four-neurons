# simple counts over printed examples (stdin)
import sys, re, collections
txt = sys.stdin.read()
blocks = re.findall(r"pole act (-?[\d.]+).*?moves: ([\d,]*)  last move col (\S+).*?\n((?:[.XO]{7}\n){6})", txt, re.S)
C = collections.Counter()
for act, mv, lc, bd in blocks:
    rows = bd.strip().split("\n")[::-1]  # row0 bottom
    if lc == 'None':
        C['start'] += 1; continue
    c = int(lc)
    h = sum(1 for r in range(6) if rows[r][c] != '.')
    r = h - 1
    below = rows[r-1][c] if r > 0 else 'floor'
    left = rows[r][c-1] if c > 0 else '|'
    right = rows[r][c+1] if c < 6 else '|'
    C['below=' + below] += 1
    C['row=%d' % r] += 1
    C['horizO=' + str(left == 'O' or right == 'O')] += 1
    C['horizX=' + str(left == 'X' or right == 'X')] += 1
for k in sorted(C): print(k, C[k])
