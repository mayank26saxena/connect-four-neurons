# mean of simple aggregate board features per examples file (stdin)
import sys, re
txt=sys.stdin.read()
blocks=re.findall(r'\[pos (\d+)\] pole act ([-\d.]+).*?moves: ([\d,]*)\s+last.*?\n((?:[.XO]{7}\n){6})',txt)
seen=set(); acc={}
def add(k,v): acc.setdefault(k,[]).append(v)
for pid,a,mv,g in blocks:
    if pid in seen: continue
    seen.add(pid)
    rows=g.strip().split('\n'); G=[[rows[5-r][c] for c in range(7)] for r in range(6)]
    nX=sum(row.count('X') for row in G); nO=sum(row.count('O') for row in G)
    add('ply',nX+nO); add('nX-nO',nX-nO)
    add('OoverX',sum(1 for r in range(1,6) for c in range(7) if G[r][c]=='O' and G[r-1][c]=='X'))
    add('XoverO',sum(1 for r in range(1,6) for c in range(7) if G[r][c]=='X' and G[r-1][c]=='O'))
    add('XX_h',sum(1 for r in range(6) for c in range(6) if G[r][c]=='X' and G[r][c+1]=='X'))
    add('OO_h',sum(1 for r in range(6) for c in range(6) if G[r][c]=='O' and G[r][c+1]=='O'))
    add('XX_v',sum(1 for r in range(5) for c in range(7) if G[r][c]=='X' and G[r+1][c]=='X'))
    add('OO_v',sum(1 for r in range(5) for c in range(7) if G[r][c]=='O' and G[r+1][c]=='O'))
    add('Xcenter',sum(1 for r in range(6) for c in (2,3,4) if G[r][c]=='X'))
    add('Ocenter',sum(1 for r in range(6) for c in (2,3,4) if G[r][c]=='O'))
    add('emptycols',sum(1 for c in range(7) if G[0][c]=='.'))
    add('Xrow0',G[0].count('X')); add('Orow0',G[0].count('O'))
    add('Xrow1',G[1].count('X')); add('Orow1',G[1].count('O'))
    hs=[sum(1 for r in range(6) if G[r][c]!='.') for c in range(7)]
    add('hspread',max(hs)-min(hs))
print('n',len(seen),' '.join('%s=%.2f'%(k,sum(v)/len(v)) for k,v in acc.items()))
