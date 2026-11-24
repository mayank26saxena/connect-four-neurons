def windows(s):
    # 4-cell windows on the down-right diagonal r + c = s
    cells = [(r, s - r) for r in range(6) if 0 <= s - r <= 6]
    return [cells[i:i + 4] for i in range(len(cells) - 3)]

def best(b):
    top = 0
    for s in (4, 5):
        for w in windows(s):
            mine = sum(1 for (r, c) in w if b.grid[r][c] == 1)
            theirs = sum(1 for (r, c) in w if b.grid[r][c] == 2)
            if theirs == 0 and mine < 4 and mine > top:
                top = mine
    return top

def fires(b):
    return best(b) >= 2 and len(b.my_playable_wins) == 0

def level(b):
    if len(b.my_playable_wins) > 0:
        return 0
    k = best(b)
    return 7 if k >= 3 else (5 if k == 2 else 0)
