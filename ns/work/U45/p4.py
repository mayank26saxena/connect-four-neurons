def centre(b):
    return b.heights[3] + b.heights[4] + b.heights[5]

def fires(b):
    if b.heights[2] != 0 or b.ply < 7:
        return False
    if b.my_playable_wins or b.their_playable_wins:
        return False
    return centre(b) >= 6 and b.heights[1] <= 2

def level(b):
    if b.heights[2] != 0 or b.ply < 6:
        return 0
    s = 2 + (centre(b) - 4)
    if b.heights[1] == 0:
        s += 1
    if b.my_playable_wins or b.their_playable_wins:
        s -= 3
    return max(0, min(9, s))
