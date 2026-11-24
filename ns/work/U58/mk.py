# build a move sequence from a board drawing. rows top->bottom, 'X' = side to move, 'O' = opponent, '.' empty
import sys
def wins(cols):
    g={}
    for c,col in enumerate(cols):
        for r,p in enumerate(col): g[(r,c)]=p
    for (r,c),p in g.items():
        for dr,dc in ((0,1),(1,0),(1,1),(1,-1)):
            if all(g.get((r+k*dr,c+k*dc))==p for k in range(4)): return True
    return False
def solve(rows):
    rows=rows[::-1]
    nx=sum(r.count('X') for r in rows); no=sum(r.count('O') for r in rows)
    # side to move X: if nx==no, X is first player; if no==nx+1, X second
    assert no in (nx,nx+1), (nx,no)
    cols=[[ch for ch in (rows[r][c] for r in range(6)) if ch!='.'] for c in range(7)]
    seq=[]
    def rec(cols,turn):  # turn = who made the last move
        if all(len(c)==0 for c in cols): return True
        for c in (3,2,4,1,5,0,6):
            if cols[c] and cols[c][-1]==turn:
                cols2=[list(x) for x in cols]; cols2[c].pop()
                if wins(cols2): continue
                seq.append(c)
                if rec(cols2,'X' if turn=='O' else 'O'): return True
                seq.pop()
        return False
    ok=rec(cols,'O')
    return ','.join(map(str,seq[::-1])) if ok else None
if __name__=='__main__':
    print(solve(sys.argv[1].split('/')))
