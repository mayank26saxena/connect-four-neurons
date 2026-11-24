def fires(b):
    return b.ply <= 16 and b.last_col in (2, 3)

def level(b):
    return 6 if fires(b) else (2 if b.ply <= 16 else 0)
