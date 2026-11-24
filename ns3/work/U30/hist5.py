import collections
ns={};eval(compile(open('hist2.py').read().split('for b in')[0],'x','exec'),ns)
parse,board=ns['parse'],ns['board']
for c in range(7):
  print('col',c)
  for b in [0,1,2,3,5,6,7,8,9]:
    hc=collections.Counter()
    for mv,_,_ in parse(f'b{b}.txt'):
        g,h=board(mv); hc[h[c]]+=1
    print(' ',b,[hc[k] for k in range(7)])
