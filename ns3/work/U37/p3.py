def fires(b):
    # column 0 has exactly one empty cell left (landing cell is the top-left corner)
    return b.heights[0] == 5

def level(b):
    if b.heights[0] == 6:
        return 0
    if b.heights[0] == 5:
        return 7
    return 2
