def g(b, r, c):
    return b.grid[r][c]

def strength(b):
    # opponent building the a1-d4 diagonal through the empty cell (2,2)
    if g(b, 2, 2) != 0:
        return 0
    a, p, q, s = g(b, 0, 0), g(b, 1, 1), g(b, 3, 3), g(b, 4, 4)
    if a == 2 and p == 2 and q == 2:
        return 3
    if p == 2 and q == 2 and s == 2:
        return 3
    if a == 2 and p == 2 and q == 0:
        return 2
    if p == 2 and q == 2 and (a == 0 or s == 0):
        return 1
    return 0

def fires(b):
    return strength(b) >= 2

def level(b):
    return [0, 2, 6, 9][strength(b)]
