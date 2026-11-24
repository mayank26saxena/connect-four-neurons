def since_kth(b, col, k):
    # plies since the k-th stone was dropped into col (1 = it was the last move)
    n = 0
    for i, m in enumerate(b.moves):
        if m == col:
            n += 1
            if n == k:
                return len(b.moves) - i
    return 99

def level(b):
    h = b.heights[4]
    if h == 6 and b.grid[5][4] == 2:
        s = since_kth(b, 4, 6)
        if b.grid[4][4] == 1:
            if s <= 1:
                return 9
            if s <= 3:
                return 7
            if s <= 5:
                return 5
            return 3
        return 5 if s <= 1 else 2
    if h == 2 and b.grid[1][4] == 2 and b.ply <= 8:
        return 6 if b.grid[0][4] == 1 else 5
    return 0

def fires(b):
    return level(b) >= 5
