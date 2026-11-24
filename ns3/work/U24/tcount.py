import sys,ast
for fn in sys.argv[1:]:
    cnt={}
    for l in open(fn):
        k=l.rindex(' [')
        mb=l[:k].strip(); s=l[k:]
        v=[x for x in ast.literal_eval(s.strip()) if x!=-32768]
        bad=sum(x<-900 for x in v); good=len(v)-bad
        win=any(x>900 for x in v)
        key=('W' if win else str(good), 'mb' if mb!='[]' else '-')
        cnt[key]=cnt.get(key,0)+1
    print(fn,sorted(cnt.items()))
