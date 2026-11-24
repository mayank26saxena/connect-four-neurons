def since_full(b):
    # number of moves played after column 0 received its 6th stone; None if col 0 not full
    n = 0
    for i, c in enumerate(b.moves):
        if c == 0:
            n += 1
            if n == 6:
                return len(b.moves) - 1 - i
    return None

def fires(b):
    k = since_full(b)
    if k is None:
        return False
    fill_ply = b.ply - k
    return k <= 2 or (k <= 10 and fill_ply <= 20)

def level(b):
    k = since_full(b)
    if k is None:
        return 1 if b.heights[0] == 5 and b.last_col == 0 else 0
    fill_ply = b.ply - k
    if k == 0:
        return 9
    if fill_ply <= 20:
        return max(2, 8 - k // 2)
    return max(1, 7 - 2 * k)
