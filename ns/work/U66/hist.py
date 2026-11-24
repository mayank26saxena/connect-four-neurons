import sys, re, collections
# reads examples output from stdin; prints per-band histogram of a single feature
feat = sys.argv[1]
txt = sys.stdin.read()
blocks = re.split(r'\n(?=\[pos )', txt)
h = collections.Counter()
for bl in blocks:
    if not bl.startswith('[pos'): continue
    lines = bl.split('\n')
    rows = [l for l in lines[1:7]]
    if len(rows) < 6: continue
    grid = list(reversed(rows))
    O_odd = sum(1 for r in grid for c,ch in enumerate(r[:7]) if ch=='O' and c%2==1)
    O_even = sum(1 for r in grid for c,ch in enumerate(r[:7]) if ch=='O' and c%2==0)
    X_odd = sum(1 for r in grid for c,ch in enumerate(r[:7]) if ch=='X' and c%2==1)
    X_even = sum(1 for r in grid for c,ch in enumerate(r[:7]) if ch=='X' and c%2==0)
    v = {'O_odd':O_odd,'O_oddfrac':round(O_odd/max(1,O_odd+O_even),1),'X_oddfrac':round(X_odd/max(1,X_odd+X_even),1),'X_odd':X_odd}[feat]
    h[v]+=1
print(sorted(h.items()))
