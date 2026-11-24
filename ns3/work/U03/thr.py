import sys,re
txt=sys.stdin.read()
cnt=[0]*7;mc=[0]*7;n=0
for line in txt.strip().split('\n'):
    m=re.search(r"their threat cells: \[(.*?)\]",line); n+=1
    cols=set(int(c) for r,c in re.findall(r"\((\d), (\d)\)",m.group(1)))
    for c in cols: cnt[c]+=1
    m2=re.search(r"all my threat cells: \[(.*?)\]",line)
    for c in set(int(c) for r,c in re.findall(r"\((\d), (\d)\)",m2.group(1))): mc[c]+=1
print("n",n,"their-threat-col frac",[round(x/n,2) for x in cnt],"my",[round(x/n,2) for x in mc])
