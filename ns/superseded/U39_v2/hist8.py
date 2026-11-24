import re
for b in range(10):
    txt=open(f'ns/work/U39/ex_b{b}.txt').read()
    ms=re.findall(r'pole act (-?[\d.]+).*?moves: ([\d,]*)',txt)
    X=[0]*7;O=[0]*7;n=0;z=0;z2=0
    for a,m in ms:
        mv=[int(x) for x in m.split(',') if x];N=len(mv);n+=1
        o=[0]*7;x=[0]*7
        for i,c in enumerate(mv):
            if i%2==N%2: x[c]+=1
            else: o[c]+=1
        for c in range(7): X[c]+=x[c];O[c]+=o[c]
        z+= (o[1]+o[4]+o[5]+o[6])<=1
        z2+= (o[1]+o[4]+o[5])==0 and o[3]>=2
    print(b,'mine',[round(v/n,1) for v in X],'theirs',[round(v/n,1) for v in O],'o1456<=1 %.2f'%(z/n),'o145=0&o3>=2 %.2f'%(z2/n))
