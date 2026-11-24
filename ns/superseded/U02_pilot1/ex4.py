import subprocess,re,sys,itertools,json
a=int(sys.argv[1]); res={}
for rest in itertools.product(range(7),repeat=3):
    s=','.join(map(str,(a,)+rest))
    o=subprocess.run(['uv','run','python','scripts/31_ns_tool.py','act','U02','--moves',s],capture_output=True,text=True).stdout
    for m in re.finditer(r'after +\d+ moves \(([0-9,]*)\): (-?[0-9.]+)',o): res[m.group(1)]=float(m.group(2))
json.dump(res,open(f'ns/work/U02/ex4_{a}.json','w'))
