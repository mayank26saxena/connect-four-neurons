def core(b):
    return b.heights[0] == 3 and b.grid[2][0] == 2

def ncol0(b):
    return sum(1 for r in range(3) if b.grid[r][0] == 2)

def fires(b):
    return core(b) and (b.last_col == 0 or ncol0(b) >= 2)

def level(b):
    if not core(b):
        return 0
    n = ncol0(b)
    lv = 1 + n
    if b.last_col == 0:
        lv += 3
    if n == 3:
        lv += 2
    return min(lv, 9)
