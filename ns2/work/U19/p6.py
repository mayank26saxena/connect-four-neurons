def score(b):
    h = b.heights[4]
    if h == 6 and b.grid[5][4] == 2:
        sc = 2.0 if b.grid[4][4] == 1 else 1.0
        theirs = sum(1 for c in range(7) if b.grid[5][c] == 2)
        mine = sum(1 for c in range(7) if b.grid[5][c] == 1)
        sc += 0.8 * (theirs - mine)
        # plies since the opponent last put a stone in the top row
        hts = [0] * 7
        last_top = -1
        for i, m in enumerate(b.moves):
            hts[m] += 1
            if hts[m] == 6:
                last_top = i
        s = len(b.moves) - last_top
        if (s % 2) == 1:
            if s <= 1:
                sc += 2.5
            elif s <= 3:
                sc += 1.2
            elif s <= 5:
                sc += 0.5
        return sc
    if h == 2 and b.grid[1][4] == 2 and b.ply <= 8:
        return 4.0 if b.grid[0][4] == 1 else 3.2
    return 0.0

def level(b):
    return max(0, min(9, int(round(score(b) * 1.3 - 1))))

def fires(b):
    return score(b) >= 3.0
