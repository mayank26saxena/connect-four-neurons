B = [2,6,4,5,5,4,4,1,5,5,3,0,4,1,3,3,3,3,5,4]
out = []
for i in range(len(B)):
    for x in range(7):
        if x == B[i]:
            continue
        C = B[:]; C[i] = x
        h = [0]*7; ok = True
        for m in C:
            h[m] += 1
            if h[m] > 6: ok = False
        if ok: out.append(",".join(map(str, C)))
print(" ".join(out))
