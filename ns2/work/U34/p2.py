def fires(b):
    # opponent's last stone sits horizontally next to my previous stone
    if len(b.moves) < 2:
        return False
    c = b.last_col
    r = b.last_row
    pc = b.moves[-2]
    pr = b.heights[pc] - 1
    if pc == c:
        pr = pr - 1
    return pr == r and abs(pc - c) == 1

def level(b):
    return 6 if fires(b) else 0
