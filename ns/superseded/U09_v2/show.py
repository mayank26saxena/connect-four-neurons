import sys,re
R,C=int(sys.argv[1]),int(sys.argv[2])
txt=open(sys.argv[3]).read()
blocks=re.findall(r"(pole act (-?[\d.]+).*?moves: ([\d,]+).*?\n((?:[.XO]{7}\n){6}))",txt)
seen=set();out=[]
for full,a,m,g in blocks:
    if m in seen: continue
    seen.add(m);ms=[int(x) for x in m.split(',')];h=ms[:-1].count(ms[-1])
    if ms[-1]==C and h==R: out.append((float(a),m,g))
out.sort()
for a,m,g in out[:: max(1,len(out)//16)]:
    print(a,m);print(g)
