# helper: remove the top stone from given columns of a board string, print new board
import sys
rows=[list(r) for r in sys.argv[1].split('/')]
for c in map(int, sys.argv[2].split(',')) if len(sys.argv)>2 and sys.argv[2] else []:
    for r in range(len(rows)):
        if rows[r][c]!='.': rows[r][c]='.'; break
print('/'.join(''.join(r) for r in rows))
