import re,sys
seen=set()
for line in open('ex.txt'):
    b=line.split()[0]
    if b not in sys.argv[1].split(','): continue
    m=re.search(r'moves: ([0-9,]+)',line).group(1); a=float(re.search(r'pole act (-?[0-9.]+)',line).group(1))
    mv=[int(x) for x in m.split(',')]
    if not (4<=len(mv)<=int(sys.argv[2])) or m in seen: continue
    seen.add(m)
    h=[0]*7; g=[[0]*7 for _ in range(6)]
    for i,c in enumerate(mv):
        g[h[c]][c]=1+(i%2); h[c]+=1
    me=1+(len(mv)%2)
    rows=[''.join('.' if g[r][c]==0 else ('X' if g[r][c]==me else 'O') for c in range(7)) for r in range(3)]
    print('%6.2f'%a, len(mv), ' '.join(reversed(rows)), m)
