from lab import *
import random
random.seed(0)
L=[x for x in items if x[0]>2.5 and x[2].ply>=14]
print(len(L))
for a,mv,b,w in random.sample(L,14):
    print(a, b.ply, 'last', b.last_col, b.last_row, 'mywins', sorted(b.my_wins), 'th', sorted(b.their_wins)); print(b.render())
