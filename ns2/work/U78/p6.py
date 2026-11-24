# cell template: for each cell, how much more often it holds their stone (O) / my stone (X)
# in the top activation band than in an ordinary band (percent tables, row 5 first)
O_TOP = [[0,0,0,0,0,0,0],[0,0,0,0,1,0,1],[0,0,1,9,21,1,1],[10,0,2,28,12,2,7],[31,1,29,61,15,8,17],[49,19,79,53,13,35,41]]
O_MID = [[2,2,8,17,9,4,4],[7,8,14,20,12,11,9],[12,14,20,23,16,17,15],[16,20,26,29,22,25,18],[27,27,29,39,34,24,25],[36,41,36,42,39,41,38]]
X_TOP = [[0,0,0,0,0,0,0],[0,0,0,0,3,0,1],[1,0,1,5,9,1,7],[1,0,7,9,28,5,15],[2,9,11,28,28,11,45],[5,53,17,46,44,19,58]]
X_MID = [[3,1,7,11,8,5,4],[5,7,14,21,16,9,5],[10,13,18,26,20,15,9],[15,15,23,28,23,17,17],[23,25,33,31,24,37,24],[38,35,39,44,36,38,36]]

def lg(x):
    # natural log via series-free approximation using repeated halving
    n = 0.0
    while x > 2.0:
        x = x / 2.0
        n += 0.6931
    while x < 1.0:
        x = x * 2.0
        n -= 0.6931
    y = (x - 1.0) / (x + 1.0)
    return n + 2.0 * (y + y * y * y / 3.0 + y ** 5 / 5.0)

def score(b):
    s = 0.0
    for r in range(6):
        for c in range(7):
            v = b.grid[r][c]
            if v == 0:
                continue
            if v == 2:
                t, m = O_TOP[5 - r][c], O_MID[5 - r][c]
            else:
                t, m = X_TOP[5 - r][c], X_MID[5 - r][c]
            s += lg((t + 2.0) / (m + 2.0))
    return s

WL = [1.0, -2.0, 0.5, 1.5, -0.5, -1.0, -1.0]
WP = [-0.5, 0.3, 0.2, 0.0, -0.3, -0.3, 0.5]
WQ = [0.0, -0.6, 1.0, 0.5, -0.4, -0.3, 0.0]

def total(b):
    if b.last_col is None or len(b.moves) < 3:
        return -20.0
    return score(b) + WL[b.last_col] + WP[b.moves[-2]] + WQ[b.moves[-3]]

def fires(b):
    t = total(b)
    # smooth and monotone in t; 0.5 at t = 1.5
    return 1.0 / (1.0 + 2.718 ** (-(t - 1.5)))

def level(b):
    return max(0, min(9, int(total(b))))
