def run(row, c, p):
    # length of the horizontal run of player p through bottom cell c if p stood there
    n = 1
    k = c - 1
    while k >= 0 and row[k] == p:
        n += 1
        k -= 1
    k = c + 1
    while k < 7 and row[k] == p:
        n += 1
        k += 1
    return n

def win_cells(row, p):
    return [c for c in range(7) if row[c] == 0 and run(row, c, p) >= 4]

def bottom_wins(b):
    # opponent's bottom-row winning cells in columns 2-6, plus my own only at column 4
    row = list(b.grid[0])
    theirs = [c for c in win_cells(row, 2) if c >= 2]
    mine = [c for c in win_cells(row, 1) if c == 4]
    return theirs + mine

def open_three_at_4(b):
    # a stone at (0,4) would give one side two bottom-row winning cells
    row = list(b.grid[0])
    if row[4] != 0:
        return False
    for p in (1, 2):
        r2 = row[:]
        r2[4] = p
        if len(win_cells(r2, p)) >= 2:
            return True
    return False

def fires(b):
    return any(c >= 2 for c in bottom_wins(b)) or open_three_at_4(b)

def level(b):
    w = [c for c in bottom_wins(b) if c >= 2]
    if 4 in w:
        return 9
    if w:
        return 7
    if open_three_at_4(b):
        return 7
    if b.heights[4] == 6:
        return 0
    return 2
