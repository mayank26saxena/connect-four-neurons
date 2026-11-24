import random, sys
def win(g,r,c,p):
    for dr,dc in ((0,1),(1,0),(1,1),(1,-1)):
        n=1
        for s in (1,-1):
            rr,cc=r+dr*s,c+dc*s
            while 0<=rr<6 and 0<=cc<7 and g[rr][cc]==p: n+=1; rr+=dr*s; cc+=dc*s
        if n>=4: return True
    return False
def play(seq):
    g=[[0]*7 for _ in range(6)]; h=[0]*7
    for i,c in enumerate(seq):
        if h[c]>=6: return False
        p=1+i%2; r=h[c]; g[r][c]=p; h[c]+=1
        if win(g,r,c,p): return False
    return True
random.seed(int(sys.argv[1])); L=int(sys.argv[2]); out=0
while out<3:
    cols=[0]*6+[2]*6+[3]*6+[4]*6+[5]*6+[6]*6
    random.shuffle(cols); pre=cols[:L]
    seq=pre+[1]*6
    if play(seq): print(','.join(map(str,seq))); out+=1
