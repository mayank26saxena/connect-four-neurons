import sys,collections
lines=[l for l in sys.stdin if l.startswith('[pos')]
P=collections.Counter(); D=collections.Counter()
for l in lines:
    mv=[int(x) for x in l.split('moves: ')[1].split()[0].split(',')]
    P[(mv[-2],mv[-1])]+=1; D[mv[-1]-mv[-2]]+=1
print('N',len(lines)); print('top pairs',P.most_common(12)); print('delta',sorted(D.items()))
