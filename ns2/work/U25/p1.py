def fires(b):
    h3 = b.heights[3]
    h4 = b.heights[4]
    if b.last_col == 4:
        return False
    return (h3 == 0 or h3 == 6) and (h4 == 0 or h4 >= 5)

def level(b):
    h3 = b.heights[3]
    h4 = b.heights[4]
    s = 0
    if h3 == 0 or h3 == 6:
        s += 4
    if h4 == 0 or h4 >= 5:
        s += 3
    if b.last_col != 4:
        s += 2
    return s
