def fires(b):
    g = b.grid
    corners = (g[0][0] == 2) + (g[0][6] == 2)
    if corners == 0:
        return False
    mine = sum(1 for c in range(1, 6) if g[0][c] == 1)
    return mine >= 2

def level(b):
    g = b.grid
    corners = (g[0][0] == 2) + (g[0][6] == 2)
    if corners == 0:
        return 0
    mine = sum(1 for c in range(1, 6) if g[0][c] == 1)
    if mine < 2:
        return 1
    v = 2 + 2 * corners + (mine - 2)
    if b.me_first:
        v += 1
    if b.ply <= 10:
        v += 2
    return min(9, v)
