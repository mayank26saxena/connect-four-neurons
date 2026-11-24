import sys,re
def parse(fn):
    L=open(fn).read().split('\n'); out=[]; i=0
    while i<len(L):
        m=re.match(r'\[pos (\d+)\] pole act (-?[\d.]+)',L[i])
        if m:
            rows=L[i+1:i+7]; out.append((int(m.group(1)),float(m.group(2)),rows[::-1])); i+=7
        else: i+=1
    return out
d={}
for fn in sys.argv[1:]:
    for p,a,r in parse(fn): d[p]=(a,r)
def h(r,c): return sum(r[k][c]!='.' for k in range(6))
tests={
 'A:(1,2)O&(2,2)X':lambda r:r[1][2]=='O' and r[2][2]=='X',
 'B:(1,4)X&(2,4)O':lambda r:r[1][4]=='X' and r[2][4]=='O',
 'A&B':lambda r:r[1][2]=='O' and r[2][2]=='X' and r[1][4]=='X' and r[2][4]=='O',
 'A|B':lambda r:(r[1][2]=='O' and r[2][2]=='X') or (r[1][4]=='X' and r[2][4]=='O'),
 'left<=1':lambda r:h(r,0)<=1 and h(r,1)<=1,
 'shiftA r2':lambda r:r[2][2]=='O' and r[3][2]=='X',
 'shiftB r2':lambda r:r[2][4]=='X' and r[3][4]=='O',
}
for name,f in tests.items():
    out=[]
    for lab,sel in [('top>2',lambda a:a>2),('fire',lambda a:0.906<a<=2),('mid .4-.9',lambda a:0.4<=a<=0.906),('low',lambda a:a<0.4)]:
        v=[f(r) for a,r in d.values() if sel(a)]
        out.append(f"{lab} {sum(v)}/{len(v)}")
    print(name, ' | '.join(out))
