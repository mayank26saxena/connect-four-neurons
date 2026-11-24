import sys, re
from collections import Counter, defaultdict
txt = sys.stdin.read()
blocks = re.findall(r"\[pos \d+\] pole act (\S+).*?moves: (\S+).*?my immediate wins (\[.*?\])  must-block (\[.*?\])\n((?:[.XO]{7}\n){6})", txt)
feat = defaultdict(lambda: defaultdict(Counter))
for act, mv, w, mb, grid in blocks:
    a = float(act); band = 'top' if a > 1.3 else ('F' if a > 0.83 else ('mid' if a > 0.39 else 'lo'))
    rows = grid.strip().split('\n')[::-1]
    ms=[int(x) for x in mv.split(',')]
    lc=ms[-1]; lr=sum(1 for x in ms if x==lc)-1
    feat['mustblock'][band][mb!='[]']+=1
    feat['mywin'][band][w!='[]']+=1
    # vertical run of theirs ending at last move
    k=0
    while lr-k>=0 and rows[lr-k][lc]=='O': k+=1
    feat['vrun_last'][band][k]+=1
    feat['lastcol'][band][lc]+=1
for f in feat:
    print(f)
    for band in ['lo','mid','F','top']:
        cnt = feat[f][band]; n = sum(cnt.values()) or 1
        print('  %4s n=%3d ' % (band, n) + ' '.join('%s:%.2f' % (k, v/n) for k, v in sorted(cnt.items(), key=str)))
