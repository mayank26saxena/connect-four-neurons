def fires(b):
    if b.heights[1] != 3:
        return 0.0
    s = 0.3
    if b.last_col == 1:
        s += 0.4
    if b.grid[2][1] == 2:
        s += 0.15
    if b.ply >= 20:
        s += 0.15
    others = [w for w in (b.my_playable_wins | b.their_playable_wins) if w[1] != 1]
    if others:
        s -= 0.3
    return max(0.0, min(1.0, s))

def level(b):
    v = fires(b)
    return int(round(v * 9))
