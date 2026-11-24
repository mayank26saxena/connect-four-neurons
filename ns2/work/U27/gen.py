import random, sys
def win(g,r,c,p):
    for dr,dc in ((0,1),(1,0),(1,1),(1,-1)):
        n=1
        for s in (1,-1):
            rr,cc=r+dr*s,c+dc*s
            while 0<=rr<6 and 0<=cc<7 and g[rr][cc]==p: n+=1; rr+=dr*s; cc+=dc*s
        if n>=4: return True
    return False
random.seed(int(sys.argv[1]))
for _ in range(int(sys.argv[2])):
    g=[[0]*7 for _ in range(6)]; h=[0]*7; mv=[]
    for t in range(42):
        p=t%2+1
        opts=[c for c in range(7) if h[c]<6 and not win(g,h[c],c,p)]
        if not opts: break
        c=random.choice(opts); g[h[c]][c]=p; h[c]+=1; mv.append(c)
    print(",".join(map(str,mv)))
