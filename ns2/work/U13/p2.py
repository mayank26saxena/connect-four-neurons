WX = {0: 3, 1: 0, 2: 2, 3: -2, 4: 3, 5: -3, 6: 0}
WO = {0: 1, 1: 0, 2: 6, 3: 3, 4: 3, 5: 6, 6: 0}
WL = {0: 1, 1: 3, 2: 0, 3: 2, 4: 5, 5: -1, 6: 5}

def opening_score(b):
    m = b.moves
    return WX[m[0]] + WX[m[2]] + WX[m[4]] + WO[m[1]] + WO[m[3]] + WL[m[5]]

def late(b):
    return b.ply in (28, 30, 32) and b.last_col in (0, 2)

def fires(b):
    if b.ply == 6:
        return opening_score(b) >= 10
    return late(b)

def level(b):
    if b.ply == 6:
        s = opening_score(b)
        return max(0, min(9, (s - 2) // 3))
    if late(b):
        return 5
    return 0
