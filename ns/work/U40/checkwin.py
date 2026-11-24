import sys
def first_win(moves):
    g=[[0]*7 for _ in range(6)]; h=[0]*7
    for i,c in enumerate(moves):
        p=1+i%2; r=h[c]; g[r][c]=p; h[c]+=1
        for dr,dc in ((0,1),(1,0),(1,1),(1,-1)):
            n=1
            for s in (1,-1):
                rr,cc=r+s*dr,c+s*dc
                while 0<=rr<6 and 0<=cc<7 and g[rr][cc]==p: n+=1; rr+=s*dr; cc+=s*dc
            if n>=4: return i+1
    return None
for a in sys.argv[1:]:
    m=[int(x) for x in a.split(',')]; print(a, first_win(m))
