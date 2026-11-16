# Trilha original sintetizada em código (livre de direitos): house leve 120 BPM, Lá menor
import numpy as np, sys, wave
SR=48000; BPM=120; BEAT=60/BPM
def env(n,a=0.005,d=0.2,s=0.6,r=0.1,sus=None):
    t=np.arange(n)/SR; e=np.ones(n)
    A=int(a*SR); e[:A]=np.linspace(0,1,A)
    return e
def kick(): n=int(0.35*SR); t=np.arange(n)/SR; f=50+90*np.exp(-t*30); ph=2*np.pi*np.cumsum(f)/SR; return np.sin(ph)*np.exp(-t*9)
def hat(o=False): n=int((0.18 if o else 0.05)*SR); t=np.arange(n)/SR; x=np.random.randn(n); x=np.diff(np.concatenate([[0],x])); return x*np.exp(-t*(18 if o else 70))*0.35
def clap(): n=int(0.2*SR); t=np.arange(n)/SR; x=np.random.randn(n); x=np.convolve(x,np.ones(8)/8,'same')-np.convolve(x,np.ones(40)/40,'same'); return x*np.exp(-t*22)*0.9
def note(f,dur,wave_='saw',det=0.0):
    n=int(dur*SR); t=np.arange(n)/SR; out=0
    for dd in (-det,0,det) if det else (0,):
        ff=f*(1+dd); ph=(t*ff)%1
        out=out+((2*ph-1) if wave_=='saw' else np.sin(2*np.pi*ff*t))
    return out/(3 if det else 1)
def lp(x,a): 
    y=np.zeros_like(x); s=0
    # filtro passa-baixa 1 polo via cumulativo
    from scipy.signal import lfilter
    return lfilter([a],[1,a-1],x)
def mtof(m): return 440*2**((m-69)/12)
def build(sec,seed=1):
    np.random.seed(seed); N=int(sec*SR)+SR; L=np.zeros(N); R=np.zeros(N)
    bars=int(np.ceil(sec/(4*BEAT)))
    prog=[[57,60,64,67],[53,57,60,64],[48,52,55,59],[55,59,62,65]]  # Am7 Fmaj7 Cmaj7 G7
    bass=[45,41,36,43]
    def add(sig,pos,g=1.0,pan=0.0):
        i=int(pos*SR); j=min(N,i+len(sig)); 
        if i>=N: return
        L[i:j]+=sig[:j-i]*g*(1-pan); R[i:j]+=sig[:j-i]*g*(1+pan)
    for b in range(bars):
        t0=b*4*BEAT; ch=prog[b%4]
        intro=b<1
        # pad
        pad=sum(note(mtof(m),4*BEAT,'saw',0.004) for m in ch)/4
        pad=lp(pad,0.03); n=len(pad); e=np.minimum(1,np.arange(n)/(0.3*SR))*np.minimum(1,(n-np.arange(n))/(0.3*SR))
        add(pad*e,t0,0.22)
        for k in range(4):
            tb=t0+k*BEAT
            if not intro: add(kick(),tb,0.9)
            add(hat(True),tb+BEAT/2,0.35 if not intro else 0.2,0.3)
            if k in (1,3) and not intro: add(clap(),tb,0.35,-0.2)
            # baixo sincopado
            if not intro:
                for off in (0.5,0.75):
                    bn=note(mtof(bass[b%4]),BEAT*0.22,'saw'); bn=lp(bn,0.08)*np.exp(-np.arange(len(bn))/SR*8)
                    add(bn,tb+off*BEAT,0.55)
            # pluck arpejo
            for s_ in range(2):
                m=ch[(k*2+s_+b)%4]+12; pl=note(mtof(m),BEAT*0.4,'saw',0.003); pl=lp(pl,0.15)*np.exp(-np.arange(len(pl))/SR*10)
                add(pl,tb+s_*BEAT/2,0.12,0.4 if s_ else -0.4)
    # eco simples no canal estéreo
    d=int(BEAT*0.75*SR); L[d:]+=R[:-d]*0.18; R[d:]+=L[:-d]*0.18
    x=np.stack([L,R],1)[:int(sec*SR)]
    fo=int(1.5*SR); x[-fo:]*=np.linspace(1,0,fo)[:,None]; x[:int(0.05*SR)]*=np.linspace(0,1,int(0.05*SR))[:,None]
    x=np.tanh(x*1.2); x/=np.abs(x).max()/0.89
    return x
if __name__=='__main__':
    sec=float(sys.argv[1]); out=sys.argv[2]; x=build(sec,int(sys.argv[3]) if len(sys.argv)>3 else 1)
    w=wave.open(out,'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((x*32767).astype('<i2').tobytes()); w.close()
