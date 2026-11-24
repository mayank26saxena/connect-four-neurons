def dead_runs(b):
    # horizontal runs of 2+ opponent stones whose both ends are my stone or the board edge
    k = 0
    for r in range(6):
        c = 0
        while c < 7:
            if b.grid[r][c] == 2:
                s = c
                while c < 7 and b.grid[r][c] == 2:
                    c += 1
                e = c
                if e - s >= 2:
                    left = s == 0 or b.grid[r][s - 1] == 1
                    right = e == 7 or b.grid[r][e] == 1
                    if left and right:
                        k += 1
            else:
                c += 1
    return k

def above_last(b):
    c = b.last_col
    if c is None:
        return False
    return (b.last_row + 1, c) in b.their_wins

def fires(b):
    return dead_runs(b) >= 2 or (dead_runs(b) >= 1 and above_last(b))

def level(b):
    k = dead_runs(b) + (2 if above_last(b) else 0)
    return min(9, 2 * k)
