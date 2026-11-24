def since_top(b):
    # plies since the opponent last put a stone in the top row (odd values only; 99 if none)
    hts = [0] * 7
    best = 99
    n = len(b.moves)
    for i, m in enumerate(b.moves):
        hts[m] += 1
        if hts[m] == 6 and (n - i) % 2 == 1:
            best = n - i
    return best

def level(b):
    h = b.heights[4]
    if h == 6 and b.grid[5][4] == 2:
        s = since_top(b)
        ox = b.grid[4][4] == 1
        if s <= 1:
            return 9 if ox else 6
        if s <= 3:
            return 7 if ox else 4
        if s <= 5:
            return 5 if ox else 3
        if s <= 7:
            return 4 if ox else 2
        return 3 if ox else 2
    if h == 2 and b.grid[1][4] == 2 and b.ply <= 8:
        return 6 if b.grid[0][4] == 1 else 5
    return 0

def fires(b):
    return level(b) >= 5
