import sys,re
exec(open("ns/work/U68/count2.py").read().split("fire=[x")[0])
fire=[x for x in parse(sys.argv[1]) if x[0]>0.349]
non=[x for x in parse(sys.argv[2])+parse(sys.argv[3]) if x[0]<=0.349 and x[2].count(",")>=8]
def top(g,c):
    h=H(g)[c]; return g[h-1][c] if h else 0
F={
 "vthree0": lambda g: H(g)[0] in (3,4,5) and all(g[H(g)[0]-1-k][0]==2 for k in range(3)),
 "h1in12": lambda g: H(g)[1] in (1,2),
 "top1O": lambda g: top(g,1)==2,
 "top0O": lambda g: top(g,0)==2,
 "top2O": lambda g: top(g,2)==2,
 "h1<h0,h2": lambda g: H(g)[1]<H(g)[0] and H(g)[1]<H(g)[2],
 "h1<h2": lambda g: H(g)[1]<H(g)[2],
 "nbrO(landing1)>=3": lambda g: H(g)[1]<6 and sum(1 for dr in (-1,0,1) for dc in (-1,0,1) if (dr or dc) and 0<=H(g)[1]+dr<6 and 0<=1+dc<7 and g[H(g)[1]+dr][1+dc]==2)>=3,
 "nbrO(landing1)>=4": lambda g: H(g)[1]<6 and sum(1 for dr in (-1,0,1) for dc in (-1,0,1) if (dr or dc) and 0<=H(g)[1]+dr<6 and 0<=1+dc<7 and g[H(g)[1]+dr][1+dc]==2)>=4,
}
for n,f in F.items():
    print("%-20s fire %.2f non %.2f"%(n, sum(f(x[1]) for x in fire)/len(fire), sum(f(x[1]) for x in non)/len(non)))
print(len(fire),len(non))
def oplay(g,c,p=2):
    h=H(g)[c]
    if h>=6: return 0
    tw=wins(g,p); g2=[row[:] for row in g]; g2[h][c]=p
    if (h,c) in tw: return 9
    return len(wins(g2,p)-tw)
for c in range(7):
  for k in (1,2,9):
    f=lambda g: oplay(g,c)>=k
    print("O plays col",c,">=",k,"fire %.2f non %.2f"%(sum(f(x[1]) for x in fire)/len(fire), sum(f(x[1]) for x in non)/len(non)))
print("=== pairs (excluding vthree0 firing)")
f2=[x for x in fire if not F["vthree0"](x[1])]
cells=[(r,c) for r in range(4) for c in range(4)]
atoms=[(r,c,v) for (r,c) in cells for v in (0,1,2)]
res=[]
for i,a in enumerate(atoms):
  for b in atoms[i+1:]:
    if (a[0],a[1])==(b[0],b[1]): continue
    f=lambda g: g[a[0]][a[1]]==a[2] and g[b[0]][b[1]]==b[2]
    pf=sum(f(x[1]) for x in f2)/len(f2); pn=sum(f(x[1]) for x in non)/len(non)
    res.append((pf/(pn+0.02),pf,pn,a,b))
res.sort(reverse=True)
for r in res[:25]: print("%.1f fire %.2f non %.2f"%r[:3], r[3], r[4])
print("=== singles low-band")
low=[x for x in parse("ns/work/U68/low.txt") if x[0]>0.349]
res=[]
for a in [(r,c,v) for r in range(6) for c in range(7) for v in (0,1,2)]:
    f=lambda g: g[a[0]][a[1]]==a[2]
    pf=sum(f(x[1]) for x in low)/len(low); pn=sum(f(x[1]) for x in non)/len(non)
    res.append((pf-pn,pf,pn,a))
res.sort()
for r in res[:8]+res[-12:]: print("%.2f fire %.2f non %.2f"%r[:3], r[3])
for n,f in F.items():
    print("%-20s low %.2f non %.2f"%(n, sum(f(x[1]) for x in low)/len(low), sum(f(x[1]) for x in non)/len(non)))
import statistics
print("ply low", statistics.mean(x[2].count(",")+1 for x in low), "non", statistics.mean(x[2].count(",")+1 for x in non))
print("=== threat cols")
for c in range(7):
    f=lambda g: any(cc==c for (r,cc) in wins(g,2))
    f2=lambda g: any(cc==c for (r,cc) in wins(g,1))
    print(c,"their: fire %.2f low %.2f non %.2f"%tuple(sum(f(x[1]) for x in grp)/len(grp) for grp in (fire,low,non)), " mine: fire %.2f low %.2f non %.2f"%tuple(sum(f2(x[1]) for x in grp)/len(grp) for grp in (fire,low,non)))
print("=== col0 cell threats")
def t(g,p,off,c=0):
    h=H(g)[c]; return h+off<6 and (h+off,c) in wins(g,p)
for p in (1,2):
  for off in (0,1,2):
    f=lambda g: t(g,p,off)
    print("p",p,"off",off,"fire %.2f low %.2f non %.2f"%tuple(sum(f(x[1]) for x in grp)/len(grp) for grp in (fire,low,non)))
for c in range(7):
    f=lambda g: t(g,1,1,c)
    print("mine above landing col",c,"fire %.2f low %.2f non %.2f"%tuple(sum(f(x[1]) for x in grp)/len(grp) for grp in (fire,low,non)))
print("=== mb combos")
def lc(x):
    m=re.search(r"last move col (\d)",x[2]); return int(m.group(1)) if m else -1
def mbcols(g): 
    h=H(g); tw=wins(g,2); return [c for c in range(7) if h[c]<6 and (h[c],c) in tw]
for name,f in (("mb any",lambda x: bool(mbcols(x[1]))),("mb col<=2",lambda x: any(c<=2 for c in mbcols(x[1]))),("mb vertical any",lambda x: any(H(x[1])[c]>=3 and all(x[1][H(x[1])[c]-1-k][c]==2 for k in range(3)) for c in mbcols(x[1]))),("mb & last<=2",lambda x: bool(mbcols(x[1])) and lc(x)<=2)):
    print(name,"fire %.2f low %.2f non %.2f"%tuple(sum(f(x) for x in grp)/len(grp) for grp in (fire,low,non)))
