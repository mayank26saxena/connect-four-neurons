def fires(b):
    # early game, me = first player
    return b.ply <= 10 and b.me_first

def level(b):
    if b.ply > 14:
        return 0
    base = 6 if b.me_first else 3
    return max(0, base - max(0, b.ply - 6) // 2)
