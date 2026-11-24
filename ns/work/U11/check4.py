# report the first move (1-based) that completes four-in-a-row in a move list, or 0
import sys
def first_four(m):
    g=[[0]*7 for _ in range(6)]; h=[0]*7
    for k,c in enumerate(m):
        p=k%2+1; r=h[c]; g[r][c]=p; h[c]+=1
        for dr,dc in ((1,0),(0,1),(1,1),(1,-1)):
            n=1
            for s in (1,-1):
                rr,cc=r+s*dr,c+s*dc
                while 0<=rr<6 and 0<=cc<7 and g[rr][cc]==p: n+=1; rr+=s*dr; cc+=s*dc
            if n>=4: return k+1
    return 0
for a in sys.argv[1:]:
    print(a, first_four(list(map(int,a.split(",")))))
