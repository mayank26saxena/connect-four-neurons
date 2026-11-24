import sys, re, collections
k=int(sys.argv[1])
txt = sys.stdin.read()
h = collections.Counter()
for m in re.finditer(r'moves: ([0-9,]*)', txt):
    mv = [int(x) for x in m.group(1).split(',') if x]
    h[mv[-k] if len(mv)>=k else None]+=1
print(sorted(h.items(), key=lambda t: str(t[0])))
