import re,sys,collections
txt=open(sys.argv[1]).read()
blocks=re.findall(r"\[pos (\d+)\] pole act ([-\d.]+).*?\n((?:[.XO]{7}\n){6})",txt)
cnt=collections.Counter(); c2=collections.Counter()
for p,a,bd in blocks:
    rows=bd.strip().split("\n")[::-1]
    h=sum(1 for r in range(6) if rows[r][0]!='.')
    top=rows[h-1][0] if h else '-'
    cnt[h]+=1; c2[(h,top)]+=1
print(len(blocks)); print(sorted(cnt.items())); print(sorted(c2.items()))
