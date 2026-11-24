def feats(b):
    g = b.grid
    a = g[0][3] == 2 and g[1][3] == 1
    c = g[1][4] == 2 and g[2][4] == 1
    d = g[1][0] == 2 and g[2][0] == 2
    return int(a) + int(c) + int(d)

def fires(b):
    return feats(b) >= 2

def level(b):
    return [0, 2, 6, 9][feats(b)]
