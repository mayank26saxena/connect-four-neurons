def fires(b):
    # opponent's last stone lands in a central-left column (1-4), directly on one of my stones,
    # in the opening/middlegame, and I have no immediate win
    if b.last_col is None or b.last_row == 0:
        return False
    if b.last_col < 1 or b.last_col > 4 or b.ply < 5 or b.ply > 24:
        return False
    if len(b.my_playable_wins) > 0:
        return False
    return b.grid[b.last_row - 1][b.last_col] == 1

def level(b):
    if not fires(b):
        return 0
    return 6 if b.last_col in (1, 2) else 4
