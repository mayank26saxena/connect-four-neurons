BAD = [{3, 4, 5}, {4, 5}, {2, 5}, {1, 3, 5}, {2, 5}, {4, 5}, {2, 3, 4}]

def violations(b):
    return sum(1 for c in range(7) if b.heights[c] in BAD[c])

def opp_pair_cols(b):
    # columns whose top two stones are both the opponent's, with room above
    out = []
    for c in range(7):
        h = b.heights[c]
        if 2 <= h <= 5 and b.grid[h - 1][c] == 2 and b.grid[h - 2][c] == 2:
            out.append(c)
    return out

def fires(b):
    return len(opp_pair_cols(b)) > 0 and violations(b) == 0

def level(b):
    p = len(opp_pair_cols(b)) > 0
    v = violations(b)
    if p and v == 0:
        return 7
    if p and v == 1:
        return 3
    if v == 0:
        return 2
    return 0
