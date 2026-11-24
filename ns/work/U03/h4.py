# my bottom-row stone in column 1 or 5 supported by a second feature next to it
def parts(b):
    g = b.grid
    n = 0
    # left: my stone at (0,1) together with my (0,2) or their stone on top (1,1)
    if g[0][1] == 1 and (g[0][2] == 1 or g[1][1] == 2):
        n += 1
    # right: my stone at (0,5) together with my (0,4) or their stone on top (1,5)
    if g[0][5] == 1 and (g[0][4] == 1 or g[1][5] == 2):
        n += 1
    return n

def fires(b):
    return parts(b) >= 1

def level(b):
    n = parts(b)
    if n == 0:
        return 0
    s = 4 + 2 * (n - 1)
    if b.heights[3] <= 1:
        s += 2
    if b.ply <= 12:
        s += 1
    return min(9, s)
