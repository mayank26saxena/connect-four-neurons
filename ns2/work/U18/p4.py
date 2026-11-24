def win_score(b):
    best = 0
    for r in range(1, 4):
        for c in range(4):
            mine = 0
            ok = True
            for k in range(4):
                v = b.grid[r][c + k]
                h = b.heights[c + k]
                if v == 2:
                    ok = False
                    break
                if v == 1:
                    if h != r + 1:
                        ok = False
                        break
                    mine += 1
                else:
                    if h < r - 1:
                        ok = False
                        break
            if ok and mine > best:
                best = mine
    return best

def fires(b):
    return win_score(b) >= 2

def level(b):
    return [0, 1, 5, 8, 9][win_score(b)]
