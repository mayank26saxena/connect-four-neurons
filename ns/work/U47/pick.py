import re, sys
for line in open(sys.argv[1]):
    m=re.match(r"\[pos (\d+)\] pole act (\S+).*moves: ([\d,]*)",line)
    if m:
        mv=[int(x) for x in m.group(3).split(',') if x!='']
        h=[0]*7
        for x in mv: h[x]+=1
        if h[1]==3: print(m.group(2), m.group(3))
