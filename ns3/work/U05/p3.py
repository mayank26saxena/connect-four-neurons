def _line_win(b, r, c, who):
    # True if placing at (r,c) completes four for `who` along a non-vertical line
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


def _col1_block(b):
    return any(c == 1 and _line_win(b, r, c, 2) for (r, c) in b.their_playable_wins)


def fires(b):
    return _col1_block(b) and len(b.their_playable_wins) == 1 and len(b.legal) > 1


def level(b):
    return 9 if fires(b) else 0
