# U51 hypothesis: fires when the side to move is LOST (opponent can force a four), found by a small bitboard search.
H = 7
BOTTOM = sum(1 << (c * H) for c in range(7))
FULLCOL = [((1 << 6) - 1) << (c * H) for c in range(7)]
ORDER = [3, 2, 4, 1, 5, 0, 6]

def winning(p):
    for s in (1, H, H - 1, H + 1):
        m = p & (p >> s)
        if m & (m >> (2 * s)):
            return True
    return False

def setup(b):
    me = 0
    mask = 0
    for r in range(6):
        for c in range(7):
            v = b.grid[r][c]
            if v:
                bit = 1 << (c * H + r)
                mask |= bit
                if v == 1:
                    me |= bit
    return me, mask

def win_moves(pos, mask):
    out = []
    for c in range(7):
        if not (mask & FULLCOL[c] & (1 << (c * H + 5))):
            mv = (mask + (1 << (c * H))) & FULLCOL[c]
            if winning(pos | mv):
                out.append(c)
    return out

def solve(pos, mask, depth, budget):
    # side to move = pos. return 1 forced win within depth, -1 forced loss, 0 unknown
    budget[0] -= 1
    moves = []
    for c in ORDER:
        if not (mask & (1 << (c * H + 5))):
            moves.append(c)
    if not moves:
        return 0
    opp = pos ^ mask
    for c in moves:
        mv = (mask + (1 << (c * H))) & FULLCOL[c]
        if winning(pos | mv):
            return 1
    if depth <= 1 or budget[0] <= 0:
        return 0
    # opponent immediate threats: must block
    threats = []
    for c in moves:
        mv = (mask + (1 << (c * H))) & FULLCOL[c]
        if winning(opp | mv):
            threats.append(c)
    if len(threats) >= 2:
        return -1
    if threats:
        moves = threats
    best = -1
    for c in moves:
        mv = (mask + (1 << (c * H))) & FULLCOL[c]
        r = -solve(opp, mask | mv, depth - 1, budget)
        if r == 1:
            return 1
        if r == 0:
            best = 0
    return best

def status(b, depth=7):
    pos, mask = setup(b)
    return solve(pos, mask, depth, [4000])

def fires(b):
    if len(b.my_wins) > 1:
        return False
    return status(b) == -1

def level(b):
    if not fires(b):
        return 0
    return min(9, 3 + b.ply // 7)
