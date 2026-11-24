import collections
ns={};eval(compile(open('hist2.py').read().split('for b in')[0],'x','exec'),ns)
parse=ns['parse']
for k in [1,2,3,4]:
  print('move -%d'%k)
  for b in [0,1,2,3,5,6,7,8,9]:
    c=collections.Counter(mv[-k] for mv,_,_ in parse(f'b{b}.txt'))
    print(' ',b,[c[i] for i in range(7)])
