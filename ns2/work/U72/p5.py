PTS = [(0.0, -0.2), (0.06, 0.5), (0.11, 1.6), (0.17, 2.3), (0.22, 2.2), (0.28, 1.5), (0.33, 0.8), (0.4, -0.3), (1.0, -1.0)]

def curve(f):
    for i in range(len(PTS) - 1):
        x0, y0 = PTS[i]
        x1, y1 = PTS[i + 1]
        if f <= x1:
            return y0 + (y1 - y0) * (f - x0) / (x1 - x0)
    return -1.0

def score(b):
    f4 = b.heights[4] / b.ply
    ramp = min(1.0, max(0.0, (b.ply - 8) / 10))
    return ramp * curve(f4) - 0.25 * (b.heights[6] - 1)

def fires(b):
    if b.last_col != 6:
        return False
    return score(b) >= 1.03

def level(b):
    if b.last_col != 6:
        return 0
    return int(max(0, min(9, round(score(b) * 3.2))))
