# ply-6 regime: additive score over the six opening moves (from act minimal pairs)
WX = {0: 3, 1: 0, 2: 2, 3: -2, 4: 3, 5: -3, 6: 0}
WO = {0: 1, 1: 0, 2: 6, 3: 3, 4: 3, 5: 6, 6: 0}
WL = {0: 1, 1: 3, 2: 0, 3: 2, 4: 5, 5: -1, 6: 5}
# later regime: column fill weights (tall 1/3/6 good, tall 2/4 bad) plus last move bonus
WH = {0: 0, 1: 1.5, 2: -1, 3: 2.5, 4: -2.5, 5: 0, 6: 2.5}
LAST = {0: 0, 2: 0, 5: -4, 1: -8, 3: -8, 4: -12, 6: -12}

def opening_score(b):
    m = b.moves
    return WX[m[0]] + WX[m[2]] + WX[m[4]] + WO[m[1]] + WO[m[3]] + WL[m[5]]

def late_score(b):
    return sum(WH[c] * b.heights[c] for c in range(7)) + LAST[b.last_col]

def fires(b):
    if b.ply == 6:
        return opening_score(b) >= 10
    if b.ply < 12:
        return False
    return late_score(b) >= 16

def level(b):
    if b.ply == 6:
        return max(0, min(9, (opening_score(b) - 2) // 3))
    if b.ply < 12:
        return 0
    return max(0, min(9, int((late_score(b) - 4) // 3)))
