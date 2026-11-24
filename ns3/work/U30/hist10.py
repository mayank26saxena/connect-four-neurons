import collections
ns={};eval(compile(open('hist2.py').read().split('for b in')[0],'x','exec'),ns)
parse,board=ns['parse'],ns['board']
for b in [0,1,2,3,5,6,7,8,9]:
    odd=[0]*7; full=[0]*7; n=0
    for mv,_,_ in parse(f'b{b}.txt'):
        g,h=board(mv); n+=1
        for c in range(7):
            if h[c]<6: odd[c]+=h[c]%2
            else: full[c]+=1
    print(b,'odd height',odd,'full',full)
