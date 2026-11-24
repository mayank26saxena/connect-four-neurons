import sys,re
lines=sys.stdin.read().split("\n")
cur=None;rows=[]
for l in lines:
    m=re.match(r"\[pos (\d+)\] pole act (\S+).*moves: (\S+)",l)
    if m:
        cur=(m.group(2),len(m.group(3).split(",")));rows=[];continue
    if cur and re.fullmatch(r"[XO.]{7}",l): rows.append(l)
    if cur and l.startswith("0123456"):
        print(cur[0],"ply",cur[1],"odd" if cur[1]%2 else "even","bottom",rows[-1]);cur=None
