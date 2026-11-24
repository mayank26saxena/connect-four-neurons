def vert(b, r, c):
    return r >= 3 and all(b.grid[r - k][c] == 2 for k in range(1, 4))

def kinds(b):
    col6 = False
    col6v = False
    othv = False
    for (r, c) in b.their_playable_wins:
        v = vert(b, r, c)
        if c == 6 and r >= 1:
            col6 = True
            if v:
                col6v = True
        elif v:
            othv = True
    return col6, col6v, othv

def fires(b):
    col6, col6v, othv = kinds(b)
    return col6 or othv

def level(b):
    col6, col6v, othv = kinds(b)
    if col6v:
        return 9
    if col6:
        return 7
    if othv:
        return 3
    return 0
