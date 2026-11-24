import re,sys,collections
txt=open(sys.argv[1]).read()
blocks=re.findall(r"\[pos (\d+)\] pole act ([-\d.]+).*?last move col (\S+).*?\n((?:[.XO]{7}\n){6})",txt)
c=collections.Counter()
for p,a,lc,bd in blocks:
    rows=bd.strip().split("\n")[::-1]
    col="".join(rows[r][0] for r in range(6)).rstrip('.')
    c[(col, lc=='0')]+=1
for k,v in sorted(c.items(), key=lambda x:-x[1]): print(k,v)
