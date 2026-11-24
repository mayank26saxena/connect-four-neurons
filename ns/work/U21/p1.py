def fires(b):
    for (r, c) in b.my_wins:
        if r == 2 and c in (1, 2, 3) and b.heights[c] < 2:
            return True
    return False

def level(b):
    best = 0
    for (r, c) in b.my_wins:
        if r == 2 and c in (1, 2, 3) and b.heights[c] < 2:
            s = 4
            for dc in (-1, 1):
                cc = c + dc
                if 0 <= cc < 7 and b.grid[3][cc] == 2:
                    s += 2
            best = max(best, s)
    return min(best, 9)
