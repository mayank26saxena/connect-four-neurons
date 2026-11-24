import sys
base=sys.argv[1].split('/'); base=['' if c=='-' else c for c in base]
for a in range(7):
  for b in range(7):
    if base[a] and base[a][-1]=='X' and base[b] and base[b][-1]=='O' and a!=b:
      c=list(base); c[a]=c[a][:-1]+'O'; c[b]=c[b][:-1]+'X'
      print('X%d<->O%d'%(a,b),'/'.join(x if x else '-' for x in c))
  # move top stone of col a to col b
for a in range(7):
  for b in range(7):
    if base[a] and a!=b and len(base[b])<6:
      c=list(base); s=c[a][-1]; c[a]=c[a][:-1]; c[b]=c[b]+s
      print('mv%s%d->%d'%(s,a,b),'/'.join(x if x else '-' for x in c))
