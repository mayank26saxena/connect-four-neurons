def fires(b):
    return len(b.legal) <= 2

def level(b):
    n = len(b.legal)
    if n <= 1:
        return 9
    if n == 2:
        return 4
    if n == 3:
        return 1
    return 0
