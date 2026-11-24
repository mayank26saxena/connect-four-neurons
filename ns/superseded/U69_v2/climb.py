# hill-climb for synthesis using the act tool (swap two same-player moves, keep legal & no earlier win)
import subprocess,random,re,sys
sys.path.insert(0,'.')
from c4n.ns import board_from_moves
def act(ms):
    o=subprocess.run(['uv','run','python','scripts/31_ns_tool.py','act','U69','--moves',','.join(map(str,ms))],capture_output=True,text=True).stdout
    v=[float(x) for x in re.findall(r'\): (-?[\d.]+)',o)]
    return v[-1] if v else -99
def ok(ms):
    h=[0]*7
    for c in ms:
        h[c]+=1
        if h[c]>6: return False
    try:
        for t in range(1,len(ms)):
            b=board_from_moves(ms[:t])
            if (b.heights[ms[t]],ms[t]) in b.my_playable_wins: return False
    except Exception: return False
    return True
random.seed(int(sys.argv[2]))
best=[int(x) for x in sys.argv[1].split(',')]; bv=act(best); print(bv,flush=True)
for it in range(int(sys.argv[3])):
    c=best[:]
    i=random.randrange(len(c)); j=random.randrange(len(c))
    if i%2!=j%2 or c[i]==c[j]: continue
    c[i],c[j]=c[j],c[i]
    if not ok(c): continue
    v=act(c)
    if v>bv:
        best,bv=c,v; print(bv,','.join(map(str,best)),flush=True)
print("BEST",bv,','.join(map(str,best)))
