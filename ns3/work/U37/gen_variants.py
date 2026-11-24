# generates single-move substitutions and same-player swaps of a base sequence (argv[1]) for act search
import sys
base=[int(x) for x in sys.argv[1].split(",")]
start=int(sys.argv[2]) if len(sys.argv)>2 else 6
out=set()
for i in range(start,len(base)):
    for c in range(7):
        s=base[:i]+[c]+base[i+1:]
        h=[0]*7; ok=True
        for x in s:
            h[x]+=1
            if h[x]>6: ok=False
        if ok and s!=base: out.add(",".join(map(str,s)))
for j in range(start,len(base)-2):
    s=base[:]; s[j],s[j+2]=s[j+2],s[j]
    if s!=base: out.add(",".join(map(str,s)))
for s in sorted(out): print(s)
