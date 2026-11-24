import sys, re
for b in range(8):
    txt = open(f"ns3/work/U08/h{b}.txt").read()
    boards = re.findall(r"\n((?:[.XO]{7}\n){6})0123456", txt)
    h4 = [0]*7; mincol=[0]*7
    for bd in boards:
        rows = bd.strip().split("\n")
        hs = [sum(1 for r in rows if r[c] != '.') for c in range(7)]
        h4[hs[4]] += 1
    print(b, len(boards), "h4 hist", h4)
