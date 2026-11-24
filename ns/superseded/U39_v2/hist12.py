import re
exec(open('ns/work/U39/hist11.py').read().split("if __name__")[0])
tests={
 'simple':lambda mv:8<=len(mv)<=16 and sum(mv.count(c) for c in (4,5,6))<=2 and mv[-1] not in (1,2),
 'simple2':lambda mv:8<=len(mv)<=16 and sum(mv.count(c) for c in (4,5,6))<=3 and mv[-1] not in (1,2) and mv.count(2)+mv.count(3)>=5,
 'S>=4 p8-16':lambda mv:8<=len(mv)<=16 and S(mv)>=4,
 'S>=3 p8-16':lambda mv:8<=len(mv)<=16 and S(mv)>=3,
}
print(list(tests))
for b in range(10):
    txt=open(f'ns/work/U39/ex_b{b}.txt').read()
    ms=[[int(x) for x in m.split(',') if x] for a,m in re.findall(r'pole act (-?[\d.]+).*?moves: ([\d,]*)',txt)]
    print(b,' '.join('%.3f'%(sum(bool(mv) and f(mv) for mv in ms)/len(ms)) for f in tests.values()))
