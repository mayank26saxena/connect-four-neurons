/pole act/ { act=$4; n=0; next }
/^[.XO]{7}$/ { row[n]=$0; n++; if(n==6){ # row[0] is top (r5)
   c2=""; for(r=5;r>=0;r--){ch=substr(row[5-r],3,1); c2=c2 ch}
   printf "%s c2(bottom-up)=%s  r1:%s r0:%s r2:%s\n", act, c2, substr(row[4],1,7), substr(row[5],1,7), substr(row[3],1,7) } }
