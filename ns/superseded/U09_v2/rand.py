import random,sys
random.seed(int(sys.argv[1]))
for _ in range(int(sys.argv[2])):
    h=[0]*7;ms=[]
    for i in range(random.randint(14,30)):
        legal=[c for c in range(7) if h[c]<6]
        c=random.choice(legal) if random.random()<0.5 else min(legal,key=lambda x:abs(x-3)+random.random()*3)
        h[c]+=1;ms.append(c)
    print(",".join(map(str,ms)))
