import re, glob, sys
sys.path.insert(0, '.')
from c4n.ns import board_from_moves
FR = [50,30,10,5,2,1,1,.5,.4,.1]
data = {}
for f in glob.glob('ns/work/U03/ex/*.txt'):
    bd = int(re.search(r'b(\d)_', f).group(1))
    for m in re.finditer(r'\[pos (\d+)\] pole act (-?[\d.]+).*?moves: ([\d,]*)', open(f).read()):
        data[int(m.group(1))] = (float(m.group(2)), [int(x) for x in m.group(3).split(',')] if m.group(3) else [], bd)
cnt = [0]*10
for v in data.values(): cnt[v[2]] += 1
items = [(a, mv, board_from_moves(mv), FR[bd]/cnt[bd]) for a, mv, bd in data.values()]
def evaluate(fn, thr=0.821, show=0):
    tp=fp=fn_=0; fps=[]; mis=[]
    for a, mv, b, w in items:
        p = bool(fn(b)); y = a > thr
        if p and y: tp+=w
        elif p: fp+=w; fps.append((a,mv,b))
        elif y: fn_+=w; mis.append((a,mv,b))
    pr = tp/max(1e-9,tp+fp); rc = tp/max(1e-9,tp+fn_)
    print(f'weighted P={pr:.2f} R={rc:.2f} F1={2*pr*rc/max(1e-9,pr+rc):.2f}  (#fp ex {len(fps)}, #miss ex {len(mis)})')
    for lst,name in ((fps,'FP'),(mis,'MISS')):
        lst.sort(key=lambda x:-x[0] if name=='MISS' else x[0])
        for a,mv,b in lst[:show]:
            print(name, a, ','.join(map(str,mv))); print(b.render())
