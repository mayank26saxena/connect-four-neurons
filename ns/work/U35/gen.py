import random, subprocess, re, sys, json
random.seed(int(sys.argv[1])); N=int(sys.argv[2])
out=[]
def wins(g,p):
    for r in range(6):
        for c in range(7):
            for dr,dc in ((0,1),(1,0),(1,1),(1,-1)):
                if all(0<=r+k*dr<6 and 0<=c+k*dc<7 and g[r+k*dr][c+k*dc]==p for k in range(4)): return True
    return False
for i in range(N):
    h=[0]*7; g=[[0]*7 for _ in range(6)]; mv=[]
    L=random.randint(10,41)
    for t in range(L):
        leg=[c for c in range(7) if h[c]<6]
        w=[1+2*(3-abs(c-3)) for c in leg]
        c=random.choices(leg,w)[0]; p=t%2+1
        g[h[c]][c]=p; h[c]+=1; mv.append(c)
        if wins(g,p): mv.pop(); break
    s=subprocess.run(["uv","run","python","scripts/31_ns_tool.py","act","U35","--moves",",".join(map(str,mv))],cwd="{REPO}",capture_output=True,text=True).stdout
    acts=[float(x) for x in re.findall(r'after\s+\d+ moves[^:]*\):\s*(-?[\d.]+)',s)]
    out.append((mv,acts))
json.dump(out,open(f"{REPO}/ns/work/U35/rand_{sys.argv[1]}.json","w"))
