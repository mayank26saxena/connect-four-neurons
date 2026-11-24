import re,sys,collections
txt=open(sys.argv[1]).read()
blocks=re.findall(r"\[pos (\d+)\] pole act ([-\d.]+).*?last move col (\S+).*?\n((?:[.XO]{7}\n){6})",txt)
cnt=collections.Counter()
for p,a,lc,bd in blocks:
    rows=bd.strip().split("\n")[::-1]
    col=[rows[r][0] for r in range(6) if rows[r][0]!='.']
    top=0
    for s in reversed(col):
        if s=='O': top+=1
        else: break
    cnt[(top, lc=='0')]+=1
print(len(blocks)); print(sorted(cnt.items()))
