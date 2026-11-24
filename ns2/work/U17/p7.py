def top_mine(b):
    h = b.heights[1]
    return h >= 1 and b.grid[h - 1][1] == 1

def top2(b):
    h = b.heights[1]
    return h >= 2 and b.grid[h - 1][1] == 1 and b.grid[h - 2][1] == 1

def opp_in(b, c):
    return sum(1 for r in range(6) if b.grid[r][c] == 2)

def route_a(b):
    h1 = b.heights[1]
    if b.heights[0] > 1 or h1 < 3 or not top_mine(b):
        return False
    if not (top2(b) or h1 >= 5):
        return False
    return opp_in(b, 2) <= 2 and (b.ply <= 22 or h1 >= 5)

def route_b(b):
    h = b.heights[1]
    return (b.last_col == 1 and h >= 2 and b.grid[h - 2][1] == 1
            and b.ply <= 7 and b.heights[0] <= 1)

def fires(b):
    return route_a(b) or route_b(b)

def level(b):
    if route_a(b):
        v = 4 + b.heights[1] - 3 - 2 * b.heights[0] - opp_in(b, 2)
        if top2(b):
            v += 1
        if b.last_col in (4, 5, 6):
            v += 2
        return max(1, min(9, v))
    if route_b(b):
        return 3
    if top_mine(b) and b.heights[1] >= 3 and b.heights[0] <= 2:
        return 1
    return 0
