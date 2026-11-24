# ply-6 regime: additive score over the six opening moves (from act minimal pairs)
WX = {0: 3, 1: 0, 2: 2, 3: -2, 4: 3, 5: -3, 6: 0}
WO = {0: 1, 1: 0, 2: 6, 3: 3, 4: 3, 5: 6, 6: 0}
WL = {0: 1, 1: 3, 2: 0, 3: 2, 4: 5, 5: -1, 6: 5}
# later regime: opponent just played column 0 (or 2) in the late middlegame, with columns 1/3/6 tall and 2/4 short
WH = {0: 0, 1: 1.5, 2: -1, 3: 2.5, 4: -2.5, 5: 0, 6: 2.5}

def opening_score(b):
    m = b.moves
    return WX[m[0]] + WX[m[2]] + WX[m[4]] + WO[m[1]] + WO[m[3]] + WL[m[5]]

def fill_score(b):
    return sum(WH[c] * b.heights[c] for c in range(7))

def late(b):
    return b.ply in (28, 30, 32) and b.last_col == 0 and fill_score(b) >= 8

def fires(b):
    if b.ply == 6:
        return opening_score(b) >= 9
    return late(b)

def level(b):
    if b.ply == 6:
        return max(0, min(9, (opening_score(b) - 2) // 3))
    if b.ply in (28, 30, 32) and b.last_col == 0:
        return max(0, min(8, int((fill_score(b) - 2) // 3)))
    return 0
