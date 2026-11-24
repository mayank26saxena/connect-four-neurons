def opp_run_top(b, c):
    h = b.heights[c]
    n = 0
    while n < h and b.grid[h - 1 - n][c] == 2:
        n += 1
    return n

def open_run(b, c):
    if b.heights[c] >= 6:
        return 0
    return opp_run_top(b, c)

def fires(b):
    # 1.0: opponent has three stacked on top of column 6 with room above (a vertical must-block in column 6)
    n6 = open_run(b, 6)
    if n6 >= 3:
        return 1.0
    if any(open_run(b, c) >= 3 for c in range(6)):
        return 0.3
    if n6 == 2:
        return 0.2
    return 0.0

def level(b):
    if open_run(b, 6) >= 3:
        return 9
    return 0
