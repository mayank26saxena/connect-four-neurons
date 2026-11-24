import re,sys
txt=open(sys.argv[1]).read()
for m in re.finditer(r"(\[pos (\d+)\] pole act ([-\d.]+).*?\n)((?:[.XO]{7}\n){6})",txt):
    rows=m.group(4).strip().split("\n")[::-1]
    col=[rows[r][0] for r in range(6) if rows[r][0]!='.']
    if not col or col[-1]!='O':
        print(m.group(1)+m.group(4))
