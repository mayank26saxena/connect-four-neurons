D = [(0, 3), (1, 4), (2, 5)]

def ndiag(b):
    return sum(1 for (r, c) in D if b.grid[r][c] == 2)

def fires(b):
    return (not b.me_first) and ndiag(b) == 3

def level(b):
    if b.me_first:
        return 0
    n = ndiag(b)
    if n < 3:
        return n
    return 5 if b.ply < 20 else 8
