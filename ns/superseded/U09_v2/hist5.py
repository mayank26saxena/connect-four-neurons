import re,collections
txt=open('ns/work/U09/ex_cache.txt').read()
blocks=re.findall(r"pole act (-?[\d.]+).*?moves: ([\d,]+).*?\n((?:[.XO]{7}\n){6})",txt)
seen=set();N=collections.Counter();H=collections.defaultdict(collections.Counter)
preds={
 'O22':lambda g:g[2][2]=='O',
 'O22&O12':lambda g:g[2][2]=='O' and g[1][2]=='O',
 'O22&O13':lambda g:g[2][2]=='O' and g[1][3]=='O',
 'O12&O13':lambda g:g[1][2]=='O' and g[1][3]=='O',
 'O22|O21 & O12|O13':lambda g:(g[2][2]=='O' or g[2][1]=='O') and (g[1][2]=='O' or g[1][3]=='O'),
 'O3of5':lambda g:sum(g[r][c]=='O' for r,c in [(2,2),(1,2),(1,3),(2,1),(3,1)])>=3,
 'X04':lambda g:g[0][4]=='X',
}
for a,m,g in blocks:
    if m in seen: continue
    seen.add(m);a=float(a);rows=g.split()[::-1]
    b='hi' if a>2 else ('fire' if a>0.909 else 'non');N[b]+=1
    for k,f in preds.items(): H[k][b]+=f(rows)
for k in preds: print(k,{b:round(100*H[k][b]/N[b]) for b in N})
