def top2(b):
    h = b.heights[1]
    return h >= 2 and b.grid[h - 1][1] == 1 and b.grid[h - 2][1] == 1

def opp_in(b, c):
    return sum(1 for r in range(6) if b.grid[r][c] == 2)

def route_a(b):
    return (b.heights[0] <= 1 and b.heights[1] >= 3 and top2(b)
            and opp_in(b, 2) <= 1 and (b.ply <= 20 or b.heights[1] >= 5))

def route_b(b):
    return (b.last_col == 1 and b.heights[1] == 2 and b.grid[0][1] == 1
            and b.ply <= 6 and b.heights[0] <= 1)

def fires(b):
    return route_a(b) or route_b(b)

def level(b):
    if route_a(b):
        v = 4 + b.heights[1] - 3 - 2 * b.heights[0]
        if b.last_col in (4, 5, 6):
            v += 2
        return max(1, min(9, v))
    if route_b(b):
        return 3
    if top2(b) and b.heights[1] >= 3 and b.heights[0] <= 2:
        return 1
    return 0
