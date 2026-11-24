import re,sys
txt=open(sys.argv[1]).read().split('\n')
rows=[]
for i,l in enumerate(txt):
    m=re.match(r'\[pos (\d+)\] pole act (-?[\d.]+)',l)
    if m:
        a=float(m.group(2)); grid=txt[i+1:i+7]
        h=[sum(1 for r in grid if r[c]!='.') for c in range(7)]
        rows.append((a,h))
for c in range(7):
    full=[a for a,h in rows if h[c]==6]; 
    print(c,"full n",len(full),"fire",sum(a>3.693 for a in full), " notfull fire", sum(a>3.693 for a,h in rows if h[c]<6))
print("total fire",sum(a>3.693 for a,h in rows))
