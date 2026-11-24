import sys,re
for f in sys.argv[1:]:
    txt=open(f).read(); n=0; M=[0]*7; T=[0]*7; P=0
    for m in re.finditer(r'moves: ([\d,]+)',txt):
        mv=[int(x) for x in m.group(1).split(',')]; n+=1; P+=len(mv)
        tm=len(mv)%2
        for i,c in enumerate(mv):
            if i%2==tm: M[c]+=1
            else: T[c]+=1
    print(f, 'ply %.1f'%(P/n), 'mine', ' '.join('%.2f'%(x/n) for x in M), '| theirs', ' '.join('%.2f'%(x/n) for x in T))
