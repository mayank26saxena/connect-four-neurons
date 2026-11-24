def col0_three(b, who):
    h = b.heights[0]
    if h < 3 or h > 5:
        return False
    return all(b.grid[h - 1 - k][0] == who for k in range(3))

def fires(b):
    return col0_three(b, 2) or col0_three(b, 1)

def level(b):
    if col0_three(b, 2):
        return 6 if b.my_playable_wins else 9
    if col0_three(b, 1):
        return 1
    return 0
