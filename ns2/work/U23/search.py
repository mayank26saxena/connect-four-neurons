import random, subprocess, re, sys, os
def win(g,r,c,p):
    for dr,dc in ((0,1),(1,0),(1,1),(1,-1)):
        n=1
        for s in (1,-1):
            rr,cc=r+s*dr,c+s*dc
            while 0<=rr<6 and 0<=cc<7 and g[rr][cc]==p:
                n+=1; rr+=s*dr; cc+=s*dc
        if n>=4: return True
    return False
def play(prefix, upto):
    g=[[0]*7 for _ in range(6)]; h=[0]*7; mv=[]
    for i,c in enumerate(prefix):
        p=1+i%2; g[h[c]][c]=p; h[c]+=1; mv.append(c)
    while len(mv)<upto:
        p=1+len(mv)%2
        opts=[c for c in range(7) if h[c]<6 and not win(g,h[c],c,p) and not win(g,h[c],c,3-p)]
        # avoid giving immediate wins is not required; just avoid completing fours
        opts=[c for c in range(7) if h[c]<6 and not win(g,h[c],c,p)]
        if not opts: break
        # bias: fill col5 early
        w=[3 if c==5 else 1 for c in opts]
        c=random.choices(opts,w)[0]
        g[h[c]][c]=p; h[c]+=1; mv.append(c)
    return mv
random.seed(int(sys.argv[1]))
prefixes=[[int(x) for x in s.split(',')] for s in sys.argv[3:]] or [[]]
best=[]
for it in range(int(sys.argv[2])):
    pre=random.choice(prefixes)
    k=random.randint(0,len(pre))
    mv=play(pre[:k], random.randint(max(24,k+1),41))
    out=subprocess.run(['uv','run','python','scripts/31_ns_tool.py','act','U23','--moves',','.join(map(str,mv))],capture_output=True,text=True).stdout
    for m in re.finditer(r'after\s+(\d+) moves \(([\d,]+)\): (-?[\d.]+)',out):
        if int(m.group(1))>=4: best.append((float(m.group(3)),m.group(2)))
    best=sorted(set(best),reverse=True)[:5]
for b in best: print(b)
