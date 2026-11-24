def run_under(b, c):
    # returns (row of top opponent cap, my run length directly under it) for the topmost O in column c that sits on my stone
    best = (None, 0)
    for r in range(1, b.heights[c]):
        if b.grid[r][c] == 2 and b.grid[r - 1][c] == 1:
            k = 0
            rr = r - 1
            while rr >= 0 and b.grid[rr][c] == 1:
                k += 1
                rr -= 1
            if k > best[1]:
                best = (r, k)
    return best

def score_cols(b):
    w = {5: 3.0, 3: 1.5, 6: 0.6, 0: 0.6, 2: 0.4, 1: 0.2, 4: 0.0}
    s = 0.0
    for c in range(7):
        r, k = run_under(b, c)
        if k > 0:
            s = max(s, w[c] * (0.6 + 0.4 * k))
    return s

def fires(b):
    return score_cols(b) >= 1.5

def level(b):
    return min(9, int(score_cols(b) * 1.5))
