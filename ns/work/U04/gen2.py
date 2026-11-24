# tail variants for the best legal prefix; keep only sequences where no move completes a four
import itertools, sys, random
argv=sys.argv[1:]; sys.argv=['x']
exec(open('ns/work/U04/legal.py').read().split('for a in')[0])
pre=[int(x) for x in argv[0].split(',')]
out=set()
for k in range(0,6):
    for fill in itertools.product([0,2],repeat=k):
        for pos in itertools.combinations(range(5+k),k):
            t=[];fi=iter(fill);p=set(pos);n6=0
            for j in range(5+k):
                t.append(next(fi) if j in p else 6)
            t.append(6)
            s=pre+t
            if s.count(2)>3: continue
            if first_win(s) is None: out.add(tuple(s))
out=list(out); random.seed(1); random.shuffle(out)
print(len(out), file=sys.stderr)
print('\n'.join(','.join(map(str,s)) for s in out[:int(argv[1])]))
