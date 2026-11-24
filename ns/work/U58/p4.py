def parts(b):
    g = b.grid
    a = g[1][0] == 2 and g[2][0] == 2              # them stacked at col 0 rows 1-2
    c4 = g[0][4] == 1 and g[1][4] == 2 and g[2][4] == 1  # col 4 bottom me/them/me
    c3 = g[0][3] == 2 and g[1][3] == 1              # col 3 bottom them/me
    return a, c4, c3

def fires(b):
    a, c4, c3 = parts(b)
    return c3 and (a or c4)

def level(b):
    a, c4, c3 = parts(b)
    n = int(a) + int(c4) + int(c3)
    if fires(b):
        return 6 + 3 * (n == 3)
    return n
