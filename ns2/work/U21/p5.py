def _k(b):
    c = b.last_col
    if c is None:
        return 0
    r = b.last_row
    if r == 0 or b.grid[r - 1][c] != 1:
        return 0
    k = r - 1
    while k >= 0 and b.grid[k][c] == 1:
        k -= 1
    if k >= 0 and b.grid[k][c] == 2:
        return 2   # their stone, my stone(s), their last stone: sandwich
    return 1       # last stone sits on my stone(s) only

def fires(b):
    return _k(b) == 2

def level(b):
    return [0, 2, 6][_k(b)]
