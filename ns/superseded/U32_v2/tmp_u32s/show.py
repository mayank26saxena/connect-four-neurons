import sys,re
exec(open('/tmp/u32s/conj.py').read().split('def h(')[0])
n=0
for p,(a,r) in sorted(d.items(), key=lambda x:-x[1][0]):
    A=r[1][2]=='O' and r[2][2]=='X'; B=r[1][4]=='X' and r[2][4]=='O'
    if a>1.5 and not (A or B):
        print(p,a); print('\n'.join(r[::-1])); n+=1
        if n>=24: break
