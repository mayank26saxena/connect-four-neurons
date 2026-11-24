import sys
sys.path.insert(0,'{REPO}')
from c4n.ns import board_from_moves, load_program
code=open(sys.argv[1]).read()
f,l=load_program(code)
g={}
exec(compile(code,"p","exec"),g)
for line in sys.stdin:
    if '->' not in line: continue
    m,a=line.split('->'); a=a.split()[0]
    b=board_from_moves([int(x) for x in m.strip().split(',')])
    print("%-32s act %6s  prog %.2f fires %s"%(m.strip(),a,g['score'](b),f(b)))
