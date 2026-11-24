def setup(b):
    return b.heights[3] == 3 and b.grid[2][3] == 2

def since(b):
    # plies since the opponent's top stone in column 3 was played (1 = just played)
    m = b.moves
    for k in range(1, len(m) + 1):
        if m[-k] == 3:
            return k
    return 99

def fires(b):
    return setup(b) and since(b) <= 3

def level(b):
    if not setup(b):
        return 0
    s = since(b)
    if s == 1:
        return 9 if b.ply <= 8 else 7
    if s == 3:
        return 5
    return 2
