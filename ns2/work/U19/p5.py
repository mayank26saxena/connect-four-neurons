def since_kth(b, col, k):
    n = 0
    for i, m in enumerate(b.moves):
        if m == col:
            n += 1
            if n == k:
                return len(b.moves) - i
    return 99

def score(b):
    h = b.heights[4]
    if h == 6 and b.grid[5][4] == 2:
        sc = 3.0 if b.grid[4][4] == 1 else 1.5
        s = since_kth(b, 4, 6)
        if s <= 1:
            sc += 3.0
        elif s <= 3:
            sc += 1.5
        elif s <= 5:
            sc += 0.7
        full = sum(1 for c in range(7) if c != 4 and b.heights[c] == 6)
        sc += 0.7 * full
        return sc
    if h == 2 and b.grid[1][4] == 2 and b.ply <= 8:
        return 5.0 if b.grid[0][4] == 1 else 4.6
    return 0.0

def level(b):
    return max(0, min(9, int(round(score(b) * 1.2 - 1))))

def fires(b):
    return score(b) >= 4.5
