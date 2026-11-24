def fires(b):
    if b.last_col is None:
        return False
    return (b.last_row, b.last_col) in [(1,3),(2,3),(0,0),(1,0),(2,0),(0,2),(3,4)]

def level(b):
    if b.last_col is None:
        return 0
    c = (b.last_row, b.last_col)
    if c == (1,3):
        return 7
    if c in [(2,3),(1,0),(0,0),(2,0),(0,2),(3,4)]:
        return 5
    return 0
