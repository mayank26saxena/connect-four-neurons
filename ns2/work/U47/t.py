import ast
band=None;st={}
for line in open('ns2/work/U47/teacher.txt'):
    if line.startswith('=='): band=line.split()[-1]; st[band]=[0,0,0,0];continue
    s=ast.literal_eval(line.strip()); best=max(s)
    st[band][0]+=1; st[band][1]+= s[1]==best; st[band][2]+= (s[1]>-900 and s[1]>=best-2); st[band][3]+= sorted(s,reverse=True).index(s[1])
for k,v in st.items(): print(k,'n',v[0],'col1 best',v[1],'col1 within2',v[2],'mean rank',v[3]/v[0])
