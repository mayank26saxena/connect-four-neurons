def _windows(b, p):
    # horizontal 4-windows with >=2 stones of p, none of the other player, every empty cell playable now
    out = []
    for r in range(6):
        for c0 in range(4):
            cells = [(r, c0 + k) for k in range(4)]
            vals = [b.grid[rr][cc] for rr, cc in cells]
            if any(v not in (0, p) for v in vals):
                continue
            n = sum(1 for v in vals if v == p)
            if n < 2:
                continue
            if all(b.heights[cc] == rr for (rr, cc), v in zip(cells, vals) if v == 0):
                out.append((r, c0, n))
    return out


def fires(b):
    return len(_windows(b, 2)) > 0


def level(b):
    w = _windows(b, 2)
    if not w:
        return 0
    return min(9, 2 + 2 * len(w) + 2 * max(n for _, _, n in w) - 4)
