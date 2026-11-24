# open diagonal lines (>=2 own stones, no opponent stone) in the lower centre-right
LINES = [
    (1, [(0, 4), (1, 3), (2, 2), (3, 1)]),  # my anti-diagonal through (0,4),(1,3)
    (2, [(0, 3), (1, 4), (2, 5), (3, 6)]),  # their diagonal through (0,3),(1,4)
    (1, [(1, 3), (2, 4), (3, 5), (4, 6)]),  # my diagonal through (1,3),(2,4)
    (1, [(0, 6), (1, 5), (2, 4), (3, 3)]),  # my anti-diagonal through (2,4),(3,3)
    (1, [(1, 3), (2, 2), (3, 1), (4, 0)]),
    (1, [(0, 2), (1, 3), (2, 4), (3, 5)]),
]

def count(b):
    n = 0
    for who, cells in LINES:
        v = [b.grid[r][c] for r, c in cells]
        if v.count(who) >= 2 and v.count(3 - who) == 0:
            n += 1
    return n

def fires(b):
    return count(b) >= 2

def level(b):
    return min(9, 2 * count(b))
