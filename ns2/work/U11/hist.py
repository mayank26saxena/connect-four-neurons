# plain per-cell occupancy histogram by activation band, from examples output on stdin
import sys
lines=sys.stdin.read().split("\n")
band=None; cnt={}; tot={}
i=0
while i<len(lines):
    l=lines[i]
    if l.startswith("=== band"):
        band=int(l.split()[2].rstrip(":"))
    if l.startswith("[pos"):
        rows=lines[i+1:i+7]
        g=[r for r in rows]
        tot[band]=tot.get(band,0)+1
        for rr in range(6):
            for c in range(7):
                ch=g[rr][c]
                key=(band,5-rr,c,ch)
                cnt[key]=cnt.get(key,0)+1
        i+=7
    i+=1
groups={"low":[0,1,2,3],"fire":[5,6,7,8,9]}
for ch in "XO.":
    print("symbol",ch)
    for gname,bs in groups.items():
        n=sum(tot.get(b,0) for b in bs)
        print(" ",gname,n)
        for r in range(5,-1,-1):
            print("   ",r," ".join("%3d"%round(100*sum(cnt.get((b,r,c,ch),0) for b in bs)/max(n,1)) for c in range(7)))
