import sys
mv=[int(x) for x in sys.argv[1].split(',')]
cols=['']*7
for i,c in enumerate(mv): cols[c]+='XO'[i%2]
print('/'.join(c if c else '-' for c in cols))
