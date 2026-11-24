# per-cell occupancy histogram in absolute colours (F = first player, S = second), plus ply parity, by band group
import sys
lines=sys.stdin.read().split("\n")
band=None; cnt={}; tot={}; par={}
i=0
while i<len(lines):
    l=lines[i]
    if l.startswith("=== band"):
        band=int(l.split()[2].rstrip(":"))
    if l.startswith("[pos"):
        g=lines[i+1:i+7]
        n=sum(ch in "XO" for r in g for ch in r[:7])
        mefirst=(n%2==0)
        tot[band]=tot.get(band,0)+1
        par[(band,mefirst)]=par.get((band,mefirst),0)+1
        for rr in range(6):
            for c in range(7):
                ch=g[rr][c]
                if ch=="X": ch="F" if mefirst else "S"
                elif ch=="O": ch="S" if mefirst else "F"
                key=(band,5-rr,c,ch)
                cnt[key]=cnt.get(key,0)+1
        i+=7
    i+=1
groups={"low":[0,1,2,3],"fire":[5,6,7,8,9]}
for gname,bs in groups.items():
    print(gname,"me_first share",round(sum(par.get((b,True),0) for b in bs)/max(1,sum(tot.get(b,0) for b in bs)),2))
for ch in "FS":
    print("symbol",ch)
    for gname,bs in groups.items():
        n=sum(tot.get(b,0) for b in bs)
        print(" ",gname,n)
        for r in range(5,-1,-1):
            print("   ",r," ".join("%3d"%round(100*sum(cnt.get((b,r,c,ch),0) for b in bs)/max(n,1)) for c in range(7)))
