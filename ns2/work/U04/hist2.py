import sys, re
from collections import Counter, defaultdict
txt = sys.stdin.read()
blocks = re.findall(r"\[pos \d+\] pole act (\S+).*?moves: (\S+).*?\n((?:[.XO]{7}\n){6})", txt)
feat = defaultdict(lambda: defaultdict(Counter))
def g(rows,r,c):
    if 0<=r<6 and 0<=c<7: return rows[r][c]
    return '#'
for act, mv, grid in blocks:
    a = float(act); band = 'F' if a > 0.83 else ('mid' if a > 0.39 else 'lo')
    if a>1.3: band='top'
    rows = grid.strip().split('\n')[::-1]
    ms=[int(x) for x in mv.split(',')]
    lc=ms[-1]; lr=sum(1 for x in ms if x==lc)-1
    feat['lastrow'][band][lr]+=1
    feat['below'][band][g(rows,lr-1,lc) if lr>0 else 'floor']+=1
    feat['left'][band][g(rows,lr,lc-1)]+=1
    feat['right'][band][g(rows,lr,lc+1)]+=1
    pc=ms[-2]; pr=sum(1 for x in ms[:-1] if x==pc)-1
    feat['dcol_last_prev'][band][abs(lc-pc)]+=1
    feat['samecol_as_mine'][band][lc==pc]+=1
    feat['h_lastcol'][band][lr+1]+=1
    # my stones count minus theirs in row 0
    feat['xcount_row0'][band][rows[0].count('X')]+=1
    feat['ocount_row0'][band][rows[0].count('O')]+=1
for f in feat:
    print(f)
    for band in ['lo','mid','F','top']:
        cnt = feat[f][band]; n = sum(cnt.values()) or 1
        print('  %4s n=%3d ' % (band, n) + ' '.join('%s:%.2f' % (k, v/n) for k, v in sorted(cnt.items(), key=str)))
