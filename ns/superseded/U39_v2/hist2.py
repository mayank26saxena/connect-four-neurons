import re
for b in range(10):
    txt=open(f'ns/work/U39/ex_b{b}.txt').read()
    ms=re.findall(r'pole act (-?[\d.]+).*?moves: ([\d,]*)',txt)
    s1=s2=s3=0;n=0;f1=f2=0
    for a,m in ms:
        mv=[int(x) for x in m.split(',') if x];h=[mv.count(c) for c in range(7)]
        n+=1;d=h[3]-h[4];e=(h[2]+h[3])-(h[4]+h[5]+h[6]);s1+=d;s2+=e
        f1+= d>=3; f2+= (h[3]>=3 and h[4]<=1)
    print(b,'h3-h4 %.1f'%(s1/n),'L-R %.1f'%(s2/n),'d>=3 %.2f'%(f1/n),'h3>=3&h4<=1 %.2f'%(f2/n))
