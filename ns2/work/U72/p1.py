def fires(b):
    if b.last_col != 6:
        return False
    return 15 <= b.ply <= 31 and b.heights[6] <= 4

def level(b):
    if b.last_col != 6:
        return 0
    s = 9 - abs(b.ply - 22) * 0.4 - max(0, b.heights[6] - 2) * 1.5
    if b.ply < 12:
        s = min(s, 1)
    return int(max(1, min(9, round(s))))
