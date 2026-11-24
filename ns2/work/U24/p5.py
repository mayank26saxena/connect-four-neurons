def fires(b):
    # the opponent threatens to win on the landing cell of the centre column (I must block in column 3)
    if b.my_playable_wins or b.landing(3) is None:
        return False
    return (b.heights[3], 3) in b.their_playable_wins

def level(b):
    if not fires(b):
        return 0
    return 9 if b.heights[3] == 5 else 5
