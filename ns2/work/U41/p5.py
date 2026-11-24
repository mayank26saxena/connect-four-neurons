W1 = [(0, 0), (1, 1), (2, 2), (3, 3)]
W2 = [(1, 1), (2, 2), (3, 3), (4, 4)]

def count(b, w):
    th = sum(1 for (r, c) in w if b.grid[r][c] == 2)
    mine = sum(1 for (r, c) in w if b.grid[r][c] == 1)
    return -1 if mine else th

def strength(b):
    t1 = count(b, W1)
    t2 = count(b, W2)
    if t1 >= 3:
        return 3
    if t2 >= 3 and b.grid[2][2] == 0:
        return 2
    if t1 == 2 and b.grid[0][0] == 2 and b.grid[1][1] == 2:
        return 1
    return 0

def fires(b):
    return strength(b) >= 1

def level(b):
    return [0, 5, 7, 9][strength(b)]
