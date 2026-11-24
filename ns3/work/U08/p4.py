def hcells(b):
    # empty bottom-row cells that would complete a horizontal four on the bottom row (either side)
    out = []
    g = b.grid
    for c in range(7):
        if g[0][c] != 0:
            continue
        for p in (1, 2):
            n = 1
            k = c - 1
            while k >= 0 and g[0][k] == p:
                n += 1
                k -= 1
            k = c + 1
            while k < 7 and g[0][k] == p:
                n += 1
                k += 1
            if n >= 4:
                out.append(c)
                break
    return out

def fires(b):
    return any(c >= 2 for c in hcells(b))

def level(b):
    cs = [c for c in hcells(b) if c >= 2]
    if 4 in cs:
        return 9
    if cs:
        return 7
    if b.heights[4] == 6:
        return 0
    return 2
