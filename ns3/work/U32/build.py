# build a move sequence from a board picture (rows top->bottom, X=me to move, O=them)
import sys
def win(g,r,c,p):
    for dr,dc in ((0,1),(1,0),(1,1),(1,-1)):
        n=1
        for s in (1,-1):
            rr,cc=r+s*dr,c+s*dc
            while 0<=rr<6 and 0<=cc<7 and g[rr][cc]==p:
                n+=1; rr+=s*dr; cc+=s*dc
        if n>=4: return True
    return False
def build(rows):
    rows=[r for r in rows if r.strip()]
    rows=rows[::-1]
    tgt=[[ '.']*7 for _ in range(6)]
    for r,line in enumerate(rows):
        for c,ch in enumerate(line): tgt[r][c]=ch
    nx=sum(l.count('X') for l in rows); no=sum(l.count('O') for l in rows)
    if nx==no: first='X'
    elif no==nx+1: first='O'
    else: raise SystemExit(f'bad counts X{nx} O{no}')
    total=nx+no
    g=[[None]*7 for _ in range(6)]; h=[0]*7; seq=[]
    def rec(p):
        if len(seq)==total: return True
        for c in (3,2,4,1,5,0,6):
            if h[c]<6 and tgt[h[c]][c]==p:
                r=h[c]
                if win(g,r,c,p) : continue
                g[r][c]=p; h[c]+=1; seq.append(c)
                if rec('O' if p=='X' else 'X'): return True
                seq.pop(); h[c]-=1; g[r][c]=None
        return False
    if not rec(first): raise SystemExit('no sequence')
    return seq
if __name__=='__main__':
    print(','.join(map(str,build(sys.argv[1].split('/')))))
