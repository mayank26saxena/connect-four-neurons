import sys,re
txt=sys.stdin.read()
ms=re.findall(r"moves: ([0-9,]+)",txt)
for c in range(7):
    d=[0]*7
    for mv in ms:
        m=[int(x) for x in mv.split(',')]; d[m.count(c)]+=1
    print(c,[round(x/len(ms),2) for x in d])
