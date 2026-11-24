def _line_win(b, r, c, who):
    # True if a stone of `who` at (r,c) completes four along a horizontal or diagonal line
    for dr, dc in ((0, 1), (1, 1), (1, -1)):
        n = 1
        for s in (1, -1):
            rr, cc = r + s * dr, c + s * dc
            while 0 <= rr < 6 and 0 <= cc < 7 and b.grid[rr][cc] == who:
                n += 1
                rr += s * dr
                cc += s * dc
        if n >= 4:
            return True
    return False


def _kind(b):
    r = b.landing(1)
    if r is None or r not in (0, 1, 5):
        return 0
    theirs = _line_win(b, r, 1, 2)
    mine = _line_win(b, r, 1, 1)
    other_mine = any(c != 1 for (rr, c) in b.my_playable_wins)
    if theirs and not other_mine and not mine:
        return 2 if len(b.their_playable_wins) == 1 else 1
    if mine:
        return 1
    return 0


def _old_fires(b):
    return _kind(b) > 0


def _early_block(b):
    return b.ply <= 10 and len(b.their_playable_wins) > 0


def fires(b):
    return _kind(b) > 0 or _early_block(b)


def level(b):
    k = _kind(b)
    if k == 2:
        return 9
    if k == 1:
        return 6
    if _early_block(b):
        return 6
    return 0
