import sys,re,subprocess
base=[int(x) for x in sys.argv[1].split(",")]
idxs=[int(x) for x in sys.argv[2].split(",")] if len(sys.argv)>2 else range(len(base))
def act(seq):
    out=subprocess.run(["uv","run","python","scripts/31_ns_tool.py","act","U06","--moves",",".join(map(str,seq))],capture_output=True,text=True).stdout
    L=[l for l in out.splitlines() if "after" in l]
    if not L: return None
    m=re.search(r"\): (-?[0-9.]+)",L[-1]); return float(m.group(1)) if m else None
print("base",act(base))
for i in idxs:
    row=[]
    for c in range(7):
        s=list(base); s[i]=c
        v=act(s); row.append("  .  " if v is None else "%+.3f"%v)
    print(i,"who=%s"%("them" if (len(base)-1-i)%2==0 else "me"),base[i]," ".join(row))
