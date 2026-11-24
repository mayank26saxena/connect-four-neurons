def fires(b):
    g = b.grid
    h2 = b.heights[2]
    h3 = b.heights[3]
    if h2 == 0:
        ok2 = True
    elif h2 == 2:
        ok2 = g[1][2] == 2
    else:
        ok2 = False
    if h3 == 0:
        ok3 = True
    elif h3 >= 2:
        ok3 = g[1][3] == 1
    else:
        ok3 = False
    return ok2 and ok3

def level(b):
    return 6 if fires(b) else 0
