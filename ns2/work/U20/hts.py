import re,sys
t=open(sys.argv[1]).read()
for sec in t.split("---")[1:]:
    for a,m in re.findall(r"pole act ([-\d.]+), program [\d.]+, moves ([\d,]+)",sec):
        mv=[int(x) for x in m.split(",")]
        print(a, len(mv), [mv.count(c) for c in range(7)])
    print("==")
