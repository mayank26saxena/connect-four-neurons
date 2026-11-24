from lab import *
from h2 import hist
print('ply<=12, last_row'); hist(lambda b: (b.ply<=12, b.last_row if b.last_row is None else min(b.last_row,2)))
print('ply<=12 lastrow>=1, last_col'); hist(lambda b: (b.ply<=12 and (b.last_row or 0)>=1, b.last_col))
print('ply<=12, lastcol stack: below stone owner'); hist(lambda b: (b.ply<=12, None if not b.last_row else b.grid[b.last_row-1][b.last_col]))
