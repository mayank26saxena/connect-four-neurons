W = [2, 0, -1, 1, 1, 1, 2]

def capscore(b):
    # columns of height exactly 2: my stone at the bottom with their stone on top
    s = 0
    for c in range(7):
        if b.heights[c] == 2 and b.grid[0][c] == 1 and b.grid[1][c] == 2:
            s += W[c]
    return s

def fires(b):
    return capscore(b) >= 3

def level(b):
    s = capscore(b)
    if s >= 5:
        return 9
    if s >= 4:
        return 7
    if s >= 3:
        return 5
    return 0
