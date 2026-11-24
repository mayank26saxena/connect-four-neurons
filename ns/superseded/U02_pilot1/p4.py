# Opening reply detector: fires on the position right after the opponent's first move in column 0, 3 or 6
# (also the openings 6,6 and 6,6,6). Elsewhere activation is a weak, diffuse function of the last stone's cell.
CELL = [  # rows 0 (bottom) .. 5 (top), columns 0..6: typical activation when the last stone landed there
    [0.06, 0.16, -0.18, 0.10, 0.05, -0.07, -0.15],
    [0.08, 0.09, -0.02, -0.05, 0.00, 0.08, 0.03],
    [0.14, -0.01, 0.05, 0.09, -0.22, 0.01, 0.00],
    [-0.02, -0.24, 0.11, 0.07, 0.11, 0.17, 0.08],
    [-0.10, -0.03, 0.27, 0.03, 0.32, 0.16, 0.17],
    [0.36, 0.40, -0.27, -0.35, 0.34, -0.16, 0.38],
]
OPEN = {3: 1.33, 0: 0.87, 6: 0.73, 5: 0.70, 1: 0.69, 2: 0.68, 4: 0.26}

def core(b):
    if b.ply == 1:
        return b.last_col in (0, 3, 6)
    return b.moves == [6, 6] or b.moves == [6, 6, 6]

def level(b):
    if b.ply == 0:
        return 0
    if b.ply == 1:
        a = OPEN[b.last_col]
    elif core(b):
        a = 1.0
    else:
        a = CELL[b.last_row][b.last_col] + (0.1 if b.ply >= 36 else 0.0)
    # map activation to 0-9
    return max(0, min(9, int((a + 0.3) / 0.16)))

def fires(b):
    # 1.0 on the core rule; otherwise a graded score below 0.5 (ranking only, never counts as firing)
    if core(b):
        return 1.0
    return level(b) / 25.0
