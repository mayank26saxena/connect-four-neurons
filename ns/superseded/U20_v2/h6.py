import sys,re,collections
exec(open('h4.py').read().split('P=parse')[0])
for fn in sys.argv[1:]:
  P=parse(fn); n=len(P)
  print(fn,n)
  # convert to P1/P2 : X=me; me is first if ply even
  for who in ('1','2'):
    print('P'+who)
    for r in range(5,-1,-1):
      row=[]
      for c in range(7):
        k=0
        for g,a,lc,mv in P:
          ply=0 if mv=='' else len(mv.split(','))
          mefirst= ply%2==0
          ch=g[r][c]
          if ch=='.': continue
          p1 = (ch=='X')==mefirst
          if (who=='1')==p1: k+=1
        row.append('%3d'%(100*k//n))
      print(' '.join(row))
