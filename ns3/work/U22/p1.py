BAD = [
    {3, 4, 5},   # col 0
    {4, 5},      # col 1
    {2, 5},      # col 2
    {1, 3, 5},   # col 3
    {2, 5},      # col 4
    {4, 5},      # col 5
    {2, 3, 4},   # col 6
]

def violations(b):
    return sum(1 for c in range(7) if b.heights[c] in BAD[c])

def fires(b):
    return violations(b) == 0

def level(b):
    v = violations(b)
    return [6, 2, 1, 0, 0, 0, 0, 0][v]
