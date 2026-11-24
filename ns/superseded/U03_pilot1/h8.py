from lab import *
for P in [8,10,12,14]:
  for H in [0,1]:
    print(P,H, end=' '); evaluate(lambda b: 3<=b.ply<=P and b.heights[3]<=H)
print('ply4-10 h3<=1 lastrow>=1'); evaluate(lambda b: 3<=b.ply<=10 and b.heights[3]<=1 and b.last_row>=1)
print('ply<=12 and stacked last move on col 1/2/4/5'); evaluate(lambda b: 3<=b.ply<=12 and b.last_row>=1 and b.last_col in (1,2,4,5) and b.heights[3]<=1)
