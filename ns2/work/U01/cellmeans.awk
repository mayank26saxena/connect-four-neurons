# input: moves activation ; compute board from me's view (player to move)
{ split($1,m,","); n=length(m); delete g; delete h
  for(i=1;i<=n;i++){c=m[i]; r=h[c]+0; h[c]=r+1; p=((i%2)==1)?1:2; g[r","c]=p}
  # player to move: if n even -> player1 to move (me=1)
  me=(n%2==0)?1:2
  for(r=0;r<3;r++)for(c=0;c<7;c++){k=r","c; v=(k in g)?((g[k]==me)?"X":"O"):"."; S[k","v]+=$2; N[k","v]++}
  tot+=$2; cnt++
}
END{ printf "mean %.3f\n", tot/cnt;
 for(r=2;r>=0;r--){ for(v in VV); for(c=0;c<7;c++){k=r","c; printf "(%d,%d) X%5.2f O%5.2f .%5.2f | ",r,c, (N[k",X"]?S[k",X"]/N[k",X"]:0),(N[k",O"]?S[k",O"]/N[k",O"]:0),(N[k",."]?S[k",."]/N[k",."]:0)}; print ""}}
