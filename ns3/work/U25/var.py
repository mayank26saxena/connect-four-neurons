import sys
base=sys.argv[1].split('/'); base=['' if c=='-' else c for c in base]
out=[]
for a in range(7):
  for b in range(7):
    if a==b: continue
    if base[a] and base[a][-1]=='X' and base[b] and base[b][-1]=='O':
      c=list(base); c[a]=c[a][:-1]; c[b]=c[b][:-1]
      out.append(('-X%d-O%d'%(a,b),'/'.join(x if x else '-' for x in c)))
for n,s in out: print(n,s)
