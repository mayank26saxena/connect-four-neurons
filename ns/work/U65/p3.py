def fires(b):
    if not b.me_first or b.ply < 2 or b.ply > 16:
        return False
    if b.heights[1] != 0:
        return False
    # opponent holds a low cell in the centre-right (cols 3-5, rows 0-1)
    return any(b.grid[r][c] == 2 for c in (3, 4, 5) for r in (0, 1))

def level(b):
    if not fires(b):
        return 0
    return max(2, 9 - b.ply // 2)
