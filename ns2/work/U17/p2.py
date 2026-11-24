def run_info(b):
    h = b.heights[1]
    run = 0
    expo = 0
    r = h - 1
    while r >= 0 and b.grid[r][1] == 1:
        run += 1
        expo += (b.grid[r][0] == 0) + (b.grid[r][2] == 0)
        r -= 1
    return h, run, expo

def fires(b):
    h, run, expo = run_info(b)
    if run == 0 or h < 3:
        return False
    return expo >= 2

def level(b):
    h, run, expo = run_info(b)
    if run == 0 or h < 2:
        return 0
    v = expo + (h - 3)
    return max(0, min(9, v))
