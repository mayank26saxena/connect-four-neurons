import json,numpy as np
r=json.load(open('ns2/report.json')); acc=r['judge']['per_unit']; rows={x['unit']:x for x in r['rows']}
def summ(excl, label):
    real=[acc[u] for u in acc if rows[u]['kind']=='neuron' and u not in excl]
    rnd=[acc[u] for u in acc if rows[u]['kind']!='neuron' and u not in excl]
    by={s:[acc[u] for u in acc if rows[u]['stratum']==s and u not in excl] for s in ('explained','unexplained','random')}
    print(f"{label}: real {np.mean(real):.3f} (n={len(real)}) random {np.mean(rnd):.3f} (n={len(rnd)}) | "+" ".join(f"{s} {np.mean(v):.3f}" for s,v in by.items()))
short={'U48','U56','U70','U74','U77'}; flag={'U59','U78','U81','U83'}
summ(set(),'all 90 (primary)')
summ(short,'excl 5 short judges')
for u in sorted(short): print(u, rows[u]['stratum'], round(acc[u],2))
def med(x): x=[v for v in x if v is not None and not np.isnan(v)]; return float(np.median(x))
R=[x for x in r['rows'] if x['unit'] not in flag]
ue=[x for x in R if x['stratum']=='unexplained']; ex=[x for x in R if x['stratum']=='explained']; rd=[x for x in R if x['stratum']=='random']; real=[x for x in R if x['kind']=='neuron']
print('flag-excluded: r_a diff',round(med([x['test_f1']-x['dict_test_f1'] for x in ue]),3),
 'r_b',round(med([x['test_f1'] for x in ex]),3),'vs',round(med([x['dict_test_f1'] for x in ex]),3),
 'r_c gap',round(med([x['test_f1'] for x in real])-med([x['test_f1'] for x in rd]),3),
 'r_d',round(med([x['sim_share'] for x in real]),3),
 'r_f',round(float(np.mean([x['test_f1']>np.percentile([y['test_f1'] for y in rd],90) for x in real])),3),
 'strata of flagged',[rows[u]['stratum'] for u in sorted(flag)])
