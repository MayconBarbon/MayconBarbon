# Club/house 120 BPM, 25 s. Drops at 3, 9, 18; end hit at 22.
import numpy as np, wave, sys
SR=48000; B=0.5; DUR=25.0; N=int(SR*DUR); L=np.zeros(N); R=np.zeros(N); rng=np.random.default_rng(3)
def add(s,t,g=1.0,pan=0.0):
    i=int(t*SR); j=min(N,i+len(s))
    if j<=i: return
    s=s[:j-i]*g; L[i:j]+=s*(1-pan); R[i:j]+=s*(1+pan)
def lp(x,fc):
    X=np.fft.rfft(x); f=np.fft.rfftfreq(len(x),1/SR); X*=1/(1+(f/fc)**4); return np.fft.irfft(X,len(x))
def hp(x,fc):
    X=np.fft.rfft(x); f=np.fft.rfftfreq(len(x),1/SR); X*=1/(1+(fc/np.maximum(f,1))**4); return np.fft.irfft(X,len(x))
def kick():
    n=int(0.38*SR); t=np.arange(n)/SR; f=45+150*np.exp(-t*35); ph=2*np.pi*np.cumsum(f)/SR
    k=np.tanh(2.2*np.sin(ph)*np.exp(-t*6.5)); k[:200]+=rng.standard_normal(200)*np.linspace(.5,0,200); return k
def clap():
    n=int(0.3*SR); x=hp(rng.standard_normal(n),900); t=np.arange(n)/SR; e=np.zeros(n)
    for k in (0,0.009,0.018,0.027): e+=np.exp(-np.clip(t-k,0,None)*(60 if k<0.027 else 16))*(t>=k)
    return x*e*0.8
def hat(o=False):
    n=int((0.22 if o else 0.045)*SR); x=hp(rng.standard_normal(n),7000); t=np.arange(n)/SR
    return x*np.exp(-t*(12 if o else 80))
def saw(f,dur,det=(1,1.007,0.993)):
    n=int(dur*SR); t=np.arange(n)/SR; s=sum(2*((f*d*t+rng.random())%1)-1 for d in det)/len(det); return s
def hz(m): return 440*2**((m-69)/12)
prog=[[57,60,64],[53,57,60],[48,52,55],[55,59,62]]; roots=[33,29,36,31]
# bass: rolling offbeat + octave
for b in range(13):
    t0=b*2.0; r=roots[b%4]
    if t0>=22: break
    for k in range(8):
        tt=t0+k*0.25
        if tt<1.0: continue
        on = (k%2==1) if tt<3 else True
        if not on: continue
        n=int(0.22*SR); t=np.arange(n)/SR; f=hz(r+(12 if k%4==3 else 0))
        s=np.tanh(1.8*(np.sin(2*np.pi*f*t)+0.6*np.sin(4*np.pi*f*t)))*np.exp(-t*7)*np.minimum(1,t/0.004)
        add(s,tt,0.30 if tt>=3 else 0.16)
    # chord stabs (offbeats), filter opens in sections
    if t0>=3.0:
        for k in (1,3,5,7):
            tt=t0+k*0.25+0.0
            fc=1800 if t0<9 else (3200 if t0<18 else 4200)
            st=sum(saw(hz(m+12),0.18) for m in prog[b%4])/3
            st=lp(st,fc)*np.exp(-np.arange(len(st))/SR*14)
            add(st,tt,0.20,pan=(-.3 if k%4==1 else .3))
    else:
        pad=lp(sum(saw(hz(m),2.0) for m in prog[b%4])/3, 500+400*b)*np.minimum(1,np.arange(int(2*SR))/SR/0.2)
        add(pad,t0,0.10)
# lead hook in 9-18 and 18-22 (simple pentatonic riff)
riff=[69,72,74,76,74,72,69,67]
for b in range(int(9/2),11):
    t0=b*2.0
    if t0<9 or t0>=22: continue
    for k,m in enumerate(riff):
        s=lp(saw(hz(m+12),0.22,(1,1.01)),3500)*np.exp(-np.arange(int(0.22*SR))/SR*9)
        add(s,t0+k*0.25,0.07,pan=0.2*np.sin(k))
# drums
for i in range(int(22/B)):
    t=i*B
    if t>=1.0: add(kick(),t,0.75 if t>=3 else 0.45)
    if t>=3.0 and i%2==1: add(clap(),t,0.32)
    if t>=2.0:
        add(hat(True),t+0.25,0.14); add(hat(),t+0.125,0.06); add(hat(),t+0.375,0.06)
# snare roll builds
def roll(t1,d=1.0):
    n=16; 
    for k in range(n):
        tt=t1-d+k*d/n; add(clap(),tt,0.05+0.25*k/n)
for t1 in (3.0,9.0,18.0): roll(t1)
def riser(t1,d=2.0):
    n=int(d*SR); x=rng.standard_normal(n); t=np.arange(n)/SR
    x=hp(x,300)*(t/d)**2.5; add(x,t1-d,0.22)
for t1 in (3.0,9.0,18.0,22.0): riser(t1, 1.5)
def boom(t,g=0.7):
    n=int(1.8*SR); tt=np.arange(n)/SR; add(np.tanh(2*np.sin(2*np.pi*(35+60*np.exp(-tt*9))*tt))*np.exp(-tt*2.2),t,g)
    add(hp(rng.standard_normal(int(0.6*SR)),2000)*np.exp(-np.arange(int(0.6*SR))/SR*6),t,0.18)
for t in (3.0,9.0,18.0,22.0): boom(t)
# drop gap: brief silence before 9 and 18 (cut drums 0.25s) handled by ducking
gate=np.ones(N)
for t1 in (8.75,17.75): gate[int(t1*SR):int((t1+0.25)*SR)]=0.25
# final chord
fin=lp(sum(saw(hz(m),3.0) for m in [48,55,60,64,67])/5,2500)*np.exp(-np.arange(int(3*SR))/SR*1.0); add(fin,22.0,0.22)
# sidechain
pump=np.ones(N)
for i in range(int(22/B)):
    t=i*B
    if t>=3.0:
        a=int(t*SR); n=int(0.22*SR); pump[a:a+n]=np.minimum(pump[a:a+n],0.35+0.65*np.linspace(0,1,n)**0.5)
# keep kick unpumped: approximate by pumping whole mix lightly
L*=pump*gate; R*=pump*gate
fo=np.ones(N); k=int(1.0*SR); fo[-k:]=np.linspace(1,0,k)**1.5; L*=fo; R*=fo
L=np.tanh(L*1.3); R=np.tanh(R*1.3)
m=max(abs(L).max(),abs(R).max()); L/=m*1.05; R/=m*1.05
w=wave.open(sys.argv[1],'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((np.stack([L,R],1)*32767).astype(np.int16).tobytes()); w.close()
