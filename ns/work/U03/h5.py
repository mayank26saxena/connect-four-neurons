# hand-weighted bottom-row pattern score (opening): centre column empty, my stones on (0,1)/(0,5)
# extended by my neighbour (0,2)/(0,4) or capped by their stone, their stone in the right corner (0,6)
def score(b):
    if b.ply < 3:
        return -9.0
    g = b.grid
    r0, r1 = g[0], g[1]
    s = 0.0
    if b.heights[3] == 0:
        s += 1.5
    elif b.heights[3] == 1:
        s += 0.5
    if r0[1] == 1:
        s += 1.0
        if r0[2] == 1:
            s += 2.0
        if r1[1] == 2:
            s += 1.0
    if r0[5] == 1:
        s += 1.0
        if r0[4] == 1:
            s += 1.5
        if r1[5] == 2:
            s += 1.5
    if r0[6] == 2:
        s += 1.0
        if r1[6] == 1:
            s += 0.5
    if r0[0] == 1:
        s -= 1.5
    elif r0[0] == 2:
        s -= 0.5
    if r0[1] == 2:
        s -= 1.0
    if r0[5] == 2:
        s -= 1.0
    if r0[6] == 1:
        s -= 0.5
    if b.ply > 16:
        s -= 1.5
    return s

def fires(b):
    return score(b) >= 3.0

def level(b):
    s = score(b)
    if s < 1.5:
        return 0
    return max(0, min(9, int(round((s - 1.5) * 2))))
