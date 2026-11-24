def fires(b):
    return b.me_first and b.last_col in (1, 4)

def level(b):
    w = {0: 1, 1: 6, 2: 4, 3: 1, 4: 7, 5: 3, 6: 1}
    if b.last_col is None:
        return 0
    v = w[b.last_col]
    if not b.me_first:
        v = v // 3
    return v
