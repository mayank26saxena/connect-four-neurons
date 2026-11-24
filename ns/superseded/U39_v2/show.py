import re,sys
b=sys.argv[1]
txt=open(f'ns/work/U39/ex_b{b}.txt').read()
blocks=txt.split('[pos ')[1:]
k=0
for bl in blocks:
    m=re.search(r'moves: ([\d,]*)',bl);mv=[int(x) for x in m.group(1).split(',') if x];h=[mv.count(c) for c in range(7)]
    if not (max(h[2],h[3])>=3 and max(h[4:])<=1):
        print(bl.strip()[:600]);print('h',h);k+=1
    if k>=12:break
