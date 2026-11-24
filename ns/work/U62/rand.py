import random,subprocess,re,sys,collections
random.seed(int(sys.argv[1]))
rows=[]
for g in range(int(sys.argv[2])):
    h=[0]*7; mv=[]
    n=random.randint(8,40)
    while len(mv)<n:
        c=random.choice([c for c in range(7) if h[c]<6]); h[c]+=1; mv.append(c)
    out=subprocess.run(['uv','run','python','scripts/31_ns_tool.py','act','U62','--moves',','.join(map(str,mv))],capture_output=True,text=True).stdout
    for m in re.finditer(r'after\s+(\d+) moves \(([\d,]+)\): ([-\d.]+)',out):
        k=int(m.group(1)); a=float(m.group(3))
        p=mv[:k]
        row=sum(1 for x in p[:-1] if x==p[-1])
        print(k%2,p[-1],row,a,k,",".join(map(str,p)))
