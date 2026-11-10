"""Alonga o 'i' final de 'Siméspi' (PSOLA/Praat) e copia os demais trechos. Mostra medições antes/depois."""
import numpy as np, parselmouth, soundfile as sf, shutil, re, sys
from parselmouth.praat import call
exec(open(sys.argv[1]).read())   # asr.py -> words()
TARGET=0.10
def voiced_runs(snd,a,b,step=0.004):
    p=snd.to_pitch(time_step=step); runs=[];cur=None
    for t in np.arange(a,b,step):
        v=p.get_value_at_time(t); vv= v and not np.isnan(v)
        if vv and cur is None: cur=t
        if not vv and cur is not None: runs.append((cur,t)); cur=None
    if cur is not None: runs.append((cur,b))
    return runs
for k in range(1,9):
    src=f"r_{k}.wav"; dst=f"a_{k}.wav"
    ws=words(src)
    hits=[w for w in ws if re.search(r"(sim|cim|mesp|mésp)", w.word.lower())]
    if not hits: shutil.copy(src,dst); print(k,"sem Siméspi"); continue
    snd=parselmouth.Sound(src)
    man=call(snd,"To Manipulation",0.01,75,300)
    dt=call(man,"Extract duration tier")
    info=[]
    for w in hits:
        runs=[r for r in voiced_runs(snd,w.start,min(snd.duration,w.end+0.18)) if r[1]-r[0]>=0.006]
        # vogal final = último trecho sonoro após o maior intervalo surdo ("sp")
        gaps=[(runs[j+1][0]-runs[j][1],j+1) for j in range(len(runs)-1)]
        if not gaps: continue
        g,j=max(gaps); a,b=runs[j]
        for r in runs[j+1:]:
            if r[0]-b<0.02: b=r[1]
        d=b-a; f=min(5.0,max(1.0,TARGET/max(d,0.01)))
        call(dt,"Add point",a-0.001,1.0); call(dt,"Add point",a,f); call(dt,"Add point",b,f); call(dt,"Add point",b+0.001,1.0)
        info.append(f"{w.word.strip()}@{w.start:.2f} i={d*1000:.0f}ms x{f:.1f}")
    call(dt,"Add point",0,1.0); call(dt,"Add point",snd.duration,1.0)
    call([man,dt],"Replace duration tier")
    out=call(man,"Get resynthesis (overlap-add)")
    out.save(dst,"WAV")
    print(k,'; '.join(info))
