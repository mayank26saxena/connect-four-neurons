import sys,collections
lines=[l for l in sys.stdin if l.startswith('[pos')]
C=collections.Counter()
for l in lines:
    mv=[int(x) for x in l.split('moves: ')[1].split()[0].split(',')]
    n=len(mv)
    C['last=prev(-2)']+= mv[-1]==mv[-2]
    C['last=-3']+= mv[-1]==mv[-3]
    C['last=-4']+= mv[-1]==mv[-4]
    C['count last col in moves']+=0
    k=mv.count(mv[-1]); C['colcount=%d'%min(k,6)]+=1
print(len(lines), sorted(C.items()))
