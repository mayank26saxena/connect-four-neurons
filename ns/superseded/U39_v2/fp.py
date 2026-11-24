import re,sys
sys.path.insert(0,'ns/work/U39')
exec(open('ns/work/U39/hist10.py').read().split('for b in range')[0])
for b in sys.argv[1:]:
    txt=open(f'ns/work/U39/ex_b{b}.txt').read()
    for bl in txt.split('[pos ')[1:]:
        m=re.search(r'moves: ([\d,]*)',bl);mv=[int(x) for x in m.group(1).split(',') if x]
        if 7<=len(mv)<=17 and S(mv)>=2:
            lines=bl.strip().split('\n')
            print(lines[0][:60],'S=',S(mv));print('\n'.join(lines[1:7]))
