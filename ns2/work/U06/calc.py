import sys
WM=[-1,-0.3,0,0,-0.5,1,0.5]; WT=[0.5,-0.3,0.5,-1,-0.5,0,0]; LB={3:3,2:2,1:2}
for s in sys.argv[1:]:
    mv=[int(x) for x in s.split(",")]
    n=len(mv); S=LB.get(mv[-1],0)
    for i,c in enumerate(mv[:-1]):
        S+= WT[c] if (n-1-i)%2==0 else WM[c]
    print("%-60s %.1f"%(s,S))
