import sys, os, glob
sys.argv=['comp.py','--dry']
src=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'comp.py')).read().replace('if __name__ == "__main__":\n    main()','')
g={'__file__':os.path.join(os.path.dirname(os.path.abspath(__file__)),'comp.py'),'__name__':'x'}
exec(src,g)
tl,k=g['build_timeline'](); tb=g['tb']
k=0
for i,(t0,t1,kind,nb,c,tr) in enumerate(tl):
    name=c[0] if not isinstance(c,list) else '+'.join(x[0][-4:] for x in c)
    print(f"{i:02d} b{k:3d} {t0:5.2f}-{t1:5.2f} {kind:7s} {tr:5s} {name}")
    k+=nb
print('total beats',k,'card at',round(tb(k),2))
used=set()
for r in tl:
    c=r[4]
    for s in (c if isinstance(c,list) else [c]): used.add(s[0])
allf={os.path.basename(p).rsplit('.',1)[0] for p in glob.glob(g['H']+'/*')+glob.glob(g['V']+'/*') if not p.endswith('.txt')}-{'PC_zoom'}; used.discard('MOCKUP')
print('faltando',sorted(allf-used), len(allf), len(used&allf))
