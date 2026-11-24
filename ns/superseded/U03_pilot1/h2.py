from lab import *
from collections import Counter
def hist(f):
    F=Counter(); N=Counter()
    for a,mv,b,w in items:
        (F if a>0.821 else N)[f(b)] += w
    keys=sorted(set(F)|set(N), key=str)
    for k in keys: print(f'  {k}: fire={F[k]:.3f} non={N[k]:.3f} rate={F[k]/(F[k]+N[k]+1e-9):.3f}')
if __name__=="__main__": print('ply'); hist(lambda b: min(b.ply//4*4, 40))
if __name__=="__main__": print('me_first'); hist(lambda b: b.me_first)
if __name__=="__main__": print('last_row'); hist(lambda b: b.last_row)
if __name__=="__main__": print('last_col'); hist(lambda b: b.last_col)
if __name__=="__main__": print('h3'); hist(lambda b: b.heights[3])
if __name__=="__main__": print('h4'); hist(lambda b: b.heights[4])
if __name__=="__main__": print('h2'); hist(lambda b: b.heights[2])
