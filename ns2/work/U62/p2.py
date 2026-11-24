def ncol0(b):
    return sum(1 for r in range(3) if b.grid[r][0] == 2)

def fires(b):
    return b.heights[0] == 3 and b.grid[2][0] == 2 and ncol0(b) >= 2

def level(b):
    if b.heights[0] != 3 or b.grid[2][0] != 2:
        return 0
    n = ncol0(b)
    if n == 3:
        lv = 8
    elif n == 2:
        lv = 5
    else:
        lv = 3
    if b.heights[1] >= 1:
        lv += 1
    return min(lv, 9)
