import sys, re, collections
feat=sys.argv[1]
txt = sys.stdin.read()
blocks = re.split(r'\n(?=\[pos )', txt)
h = collections.Counter(); n=0
for bl in blocks:
    if not bl.startswith('[pos'): continue
    rows = bl.split('\n')[1:7]
    g = list(reversed(rows))
    def cnt(ch, cols): return sum(1 for r in range(6) for c in cols if g[r][c]==ch)
    v = {'O15':cnt('O',[1,5]), 'O3':cnt('O',[3]), 'O026':cnt('O',[0,2,6]), 'X15':cnt('X',[1,5]),'O4':cnt('O',[4]),'X4':cnt('X',[4]),
         'par':(cnt('O',range(7))+cnt('X',range(7)))%2, 'ply':(cnt('O',range(7))+cnt('X',range(7)))//5*5}[feat]
    h[v]+=1; n+=1
print(n, sorted(h.items()))
