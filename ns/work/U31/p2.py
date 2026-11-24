def run_below(b, r, c):
    k = 0
    rr = r - 1
    while rr >= 0 and b.grid[rr][c] == 1:
        k += 1
        rr -= 1
    return k

def strength(b):
    s = 0
    if b.grid[3][5] == 2:
        k = run_below(b, 3, 5)
        if k >= 1:
            s = max(s, 4 + 2 * k)
    if b.grid[3][3] == 2:
        k = run_below(b, 3, 3)
        if k >= 2:
            s = max(s, 2 + 2 * k)
    return s

def fires(b):
    return strength(b) >= 6

def level(b):
    return min(9, strength(b))
