def nbr(b):
    if b.last_col is None:
        return 0
    r, c = b.last_row, b.last_col
    n = 0
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            rr, cc = r + dr, c + dc
            if (dr or dc) and 0 <= rr < 6 and 0 <= cc < 7 and b.grid[rr][cc] == 1:
                n += 1
    return n

def fires(b):
    return nbr(b) >= 3 and len(b.my_playable_wins) == 0 and b.ply <= 28

def level(b):
    if len(b.my_playable_wins) > 0:
        return 0
    return min(9, 2 * nbr(b))
