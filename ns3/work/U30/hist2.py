import re,collections
def parse(fn):
    out=[]
    for line in open(fn):
        m=re.search(r'moves: ([\d,]+)\s+last move col (\d)\s+my immediate wins \[(.*?)\]\s+must-block \[(.*?)\]',line)
        if m: out.append(([int(x) for x in m.group(1).split(',')],m.group(3)!='',m.group(4)!=''))
    return out
def board(mv):
    g=[[0]*7 for _ in range(6)];h=[0]*7
    for i,c in enumerate(mv):
        g[h[c]][c]=1+(i%2);h[c]+=1
    return g,h
for b in [0,1,2,3,5,6,7,8,9]:
    gs=parse(f'b{b}.txt')
    mw=sum(x[1] for x in gs); mb=sum(x[2] for x in gs)
    st=collections.Counter()
    for mv,_,_ in gs:
        g,h=board(mv); c=mv[-1]; r=h[c]-1; p=g[r][c]; k=0
        while r-k>=0 and g[r-k][c]==p: k+=1
        st[k]+=1
    print(b,'mywin',mw,'mustblock',mb,'laststack',sorted(st.items()))
