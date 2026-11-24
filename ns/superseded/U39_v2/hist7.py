import re
def tops(mv):
    n=len(mv);t={}
    for i,c in enumerate(mv): t[c]='X' if i%2==n%2 else 'O'
    return t
for b in range(10):
    txt=open(f'ns/work/U39/ex_b{b}.txt').read()
    ms=re.findall(r'pole act (-?[\d.]+).*?moves: ([\d,]*)',txt)
    cnt={}
    for a,m in ms:
        mv=[int(x) for x in m.split(',') if x];t=tops(mv)
        for c in range(7):
            k=(c,t.get(c,'.'));cnt[k]=cnt.get(k,0)+1
    print(b,' '.join('%d:%2d/%2d/%2d'%(c,cnt.get((c,'X'),0),cnt.get((c,'O'),0),cnt.get((c,'.'),0)) for c in range(7)))
