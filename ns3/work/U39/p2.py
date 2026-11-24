def col1_fresh(b):
    # last stone went in column 1 and I (player to move) have no stone in column 1
    if b.last_col != 1:
        return False
    return all(b.grid[r][1] != 1 for r in range(6))

def opening4(b):
    if b.ply != 4:
        return False
    return len(set(b.moves)) >= 3

def fires(b):
    return col1_fresh(b) or opening4(b)

def level(b):
    if col1_fresh(b):
        n = b.heights[1]
        if n == 1:
            if b.ply <= 4:
                return 9
            if b.ply <= 7:
                return 7
            return 5
        return 3
    if opening4(b):
        return 3
    return 0
