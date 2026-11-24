import random, subprocess, re, sys
from c4n.ns import board_from_moves
random.seed(int(sys.argv[1])); N = int(sys.argv[2])
def valid(seq):
    # no move completes a four: check each prefix's landing cell against winner cells
    for i in range(len(seq)):
        b = board_from_moves(seq[:i])
        c = seq[i]
        if c not in b.legal: return False
        if (b.landing(c), c) in b.my_wins: return False
    return True
def act(seq):
    out = subprocess.run(['uv','run','python','scripts/31_ns_tool.py','act','U02','--moves',','.join(map(str,seq))],capture_output=True,text=True).stdout
    vals = re.findall(r'after\s+(\d+) moves.*?: (-?[0-9.]+)', out)
    return [(int(k), float(v)) for k, v in vals]
seeds = [
 [4,4,0,2,3,4,4,3,3,2,3,3,0,6,3,4,0,0,2,2,2,2,6,0,6,0,6,6],
 [2,2,0,1,2,3,1,1,3,1,1,2,0,5,6,4,2,4,3,3,3,3,1,6,2,0,0,0,6,0,6,6,6],
 [4,4,3,2,2,4,4,1,3,3,5,6,3,2,2,6,0,0,0,4,4,6,6,2,2,3,3,0,6,6,0,0],
]
best = (0, None)
for it in range(N):
    mode = random.random()
    if mode < 0.5:
        cols = [0,3] + random.sample([2,4,6,1,5], random.choice([2,3]))
        random.shuffle(cols)
        seq = []
        for c in cols: seq += [c]*6
        seq += [random.choice([1,5,1,5,4]) for _ in range(random.randint(0,4))]
    else:
        s = list(random.choice(seeds)); k = random.randint(len(s)-10, len(s))
        seq = s[:k]
        while len(seq) < 40:
            b = board_from_moves(seq)
            safe = [c for c in b.legal if (b.landing(c), c) not in b.my_wins]
            if not safe or len(b.legal) <= 1: break
            seq.append(random.choice(safe))
            if random.random() < 0.08: break
    if not valid(seq): continue
    vals = act(seq)
    for k, v in vals:
        if k >= 4 and v > best[0]:
            best = (v, seq[:k]); print(round(v,3), ','.join(map(str, seq[:k])), flush=True)
