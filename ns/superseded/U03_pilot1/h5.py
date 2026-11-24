from lab import *
from h2 import hist
print('my_wins'); hist(lambda b: min(len(b.my_wins),4))
print('their_wins'); hist(lambda b: min(len(b.their_wins),4))
print('myplay'); hist(lambda b: len(b.my_playable_wins))
print('theirplay'); hist(lambda b: len(b.their_playable_wins))
print('n legal'); hist(lambda b: len(b.legal))
print('empty cols'); hist(lambda b: sum(h==0 for h in b.heights))
print('bottom mine'); hist(lambda b: sum(b.grid[0][c]==1 for c in range(7)))
print('bottom theirs'); hist(lambda b: sum(b.grid[0][c]==2 for c in range(7)))
