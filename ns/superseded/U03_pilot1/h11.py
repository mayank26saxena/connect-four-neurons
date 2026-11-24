from lab import *
base=lambda b: 3<=b.ply<=10 and b.heights[3]==0
evaluate(base)
evaluate(lambda b: base(b) and (b.grid[0][2]==1 or b.grid[0][4]==1))
evaluate(lambda b: base(b) and b.last_row>=1)
evaluate(lambda b: base(b) and b.me_first)
evaluate(lambda b: base(b) and (b.grid[0][2]==1 or b.grid[0][4]==1 or b.grid[0][1]==1 or b.grid[0][5]==1))
evaluate(lambda b: 3<=b.ply<=12 and b.heights[3]<=1 and sum(b.grid[0][c]==1 for c in range(7))>=2 and b.grid[0][3]!=1)
