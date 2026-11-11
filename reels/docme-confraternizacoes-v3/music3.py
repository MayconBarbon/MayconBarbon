# Lounge / deep house, upbeat. 122 BPM-feel on the 120 grid (beat = 0.5 s). 25 s.
import numpy as np, wave, sys
SR=48000; B=0.5; DUR=25.0; N=int(SR*DUR); L=np.zeros(N); R=np.zeros(N); rng=np.random.default_rng(11)
def add(s,t,g=1.0,pan=0.0):
    i=int(round(t*SR)); j=min(N,i+len(s))
    if j<=i or i<0: return
    s=s[:j-i]*g; L[i:j]+=s*(1-pan); R[i:j]+=s*(1+pan)
def filt(x,lo=None,hi=None):
    X=np.fft.rfft(x); f=np.fft.rfftfreq(len(x),1/SR)
    if hi: X*=1/(1+(f/hi)**4)
    if lo: X*=1/(1+(lo/np.maximum(f,1))**4)
    return np.fft.irfft(X,len(x))
def hz(m): return 440*2**((m-69)/12)
def rhodes(f,dur):
    n=int(dur*SR); t=np.arange(n)/SR
    mod=np.sin(2*np.pi*f*14*t)*np.exp(-t*9)*1.6          # FM bell attack
    s=np.sin(2*np.pi*f*t+mod)+0.25*np.sin(2*np.pi*2*f*t)*np.exp(-t*3)
    trem=1+0.18*np.sin(2*np.pi*5.2*t)
    return s*np.exp(-t*1.3)*np.minimum(1,t/0.004)*np.minimum(1,(dur-t)/0.05)*trem
def kick():
    n=int(0.32*SR); t=np.arange(n)/SR; f=48+95*np.exp(-t*30); ph=2*np.pi*np.cumsum(f)/SR
    return np.tanh(1.6*np.sin(ph)*np.exp(-t*8))
def clap():
    n=int(0.45*SR); t=np.arange(n)/SR; x=filt(rng.standard_normal(n),lo=1100,hi=7000); e=np.zeros(n)
    for k in (0,0.008,0.017): e+=np.exp(-np.clip(t-k,0,None)*70)*(t>=k)
    e+=0.25*np.exp(-t*9)  # room tail
    return x*e*0.7
def shaker(acc):
    n=int(0.07*SR); t=np.arange(n)/SR; x=filt(rng.standard_normal(n),lo=5000)
    return x*np.minimum(1,t/0.01)*np.exp(-t*45)*(1.0 if acc else 0.55)
def ohat():
    n=int(0.25*SR); t=np.arange(n)/SR; return filt(rng.standard_normal(n),lo=8000)*np.exp(-t*13)
def conga(f):
    n=int(0.2*SR); t=np.arange(n)/SR; return np.sin(2*np.pi*(f+40*np.exp(-t*40))*t)*np.exp(-t*16)
# jazzy progression, 2 s per chord: Dm9  G13  Cmaj9  Am9
prog=[[50,53,57,60,64],[55,59,64,65,69],[48,52,55,59,62],[45,48,52,55,59]]
roots=[38,43,36,33]
for b in range(13):
    t0=b*2.0
    if t0>=22: break
    c=prog[b%4]
    # rhodes comping: hit on 1 and the "and" of 2, + push before next bar
    for off,d,g in ((0.0,0.7,1.0),(0.75,0.5,0.7),(1.25,0.6,0.85),(1.75,0.25,0.5)):
        if t0+off<0.5: continue
        for k,m in enumerate(c):
            add(rhodes(hz(m),d),t0+off+0.004*k,0.035*g*(0.6 if t0<3 else 1.0),pan=(-0.35+0.17*k))
    # deep bass: syncopated
    if t0>=1.0:
        r=roots[b%4]
        pat=[(0.0,0.22,0),(0.75,0.18,0),(1.0,0.2,12),(1.5,0.2,0),(1.75,0.2,7)]
        for off,d,iv in pat:
            if t0<3 and off not in (0.0,1.0): continue
            n=int(d*SR); t=np.arange(n)/SR; f=hz(r+iv)
            s=np.tanh(1.3*(np.sin(2*np.pi*f*t)+0.3*np.sin(4*np.pi*f*t)))*np.minimum(1,t/0.005)*np.exp(-t*4)
            add(s,t0+off,0.36 if t0>=3 else 0.2)
# pluck/marimba hook in 9-22
hook=[74,76,79,76,74,72,74,0, 74,76,79,81,79,76,74,0]
for b in range(5,11):
    t0=b*2.0
    if t0>=22: break
    for k,m in enumerate(hook[(b%2)*8:(b%2)*8+8]):
        if m==0: continue
        n=int(0.25*SR); t=np.arange(n)/SR; f=hz(m)
        s=(np.sin(2*np.pi*f*t)+0.4*np.sin(2*np.pi*4*f*t)*np.exp(-t*30))*np.exp(-t*11)
        add(s,t0+k*0.25,0.07,pan=0.25); add(s,t0+k*0.25+0.375,0.025,pan=-0.3)  # dotted-8th echo
# vocal-ish pad "ooh" (formant-filtered saw) in 18-22
for b in (9,10):
    t0=b*2.0; c=prog[b%4]; n=int(2*SR); t=np.arange(n)/SR
    s=sum(2*((hz(m+12)*t*d)%1)-1 for m in c[1:4] for d in (1,1.006))/6
    s=filt(s,lo=500,hi=1400)*np.minimum(1,t/0.3)*np.minimum(1,(2-t)/0.3)
    add(s,t0,0.12)
# drums with swing on 16ths
SW=0.018
for i in range(int(22/0.125)):
    t=i*0.125+(SW if i%2==1 else 0)
    if t>=22: break
    beat=i%4==0; q=i//4
    if beat and t>=1.0: add(kick(),t,0.62 if t>=3 else 0.35)
    if beat and q%2==1 and t>=3: add(clap(),t,0.26)
    if t>=1.5: add(shaker(i%2==0),t,0.10,pan=0.3)
    if i%4==2 and t>=3: add(ohat(),t,0.11,pan=-0.2)
    if t>=9 and i%16 in (3,6,11,14): add(conga(220 if i%16 in (3,11) else 180),t,0.16,pan=-0.4)
# transitions: filtered sweep + soft impact
def sweep(t1,d=1.5):
    n=int(d*SR); t=np.arange(n)/SR; x=filt(rng.standard_normal(n),lo=600,hi=9000)*(t/d)**2; add(x,t1-d,0.12)
for t1 in (3.0,9.0,18.0,22.0): sweep(t1)
def impact(t,g=0.45):
    n=int(1.2*SR); tt=np.arange(n)/SR; add(np.sin(2*np.pi*(40+50*np.exp(-tt*10))*tt)*np.exp(-tt*3),t,g)
for t in (3.0,9.0,18.0,22.0): impact(t)
# final chord ring (Cmaj9) + logo shimmer
for k,m in enumerate([48,55,59,62,64,71]): add(rhodes(hz(m),3.0),22.0+0.01*k,0.06)
for k,m in enumerate([83,86,88,91]): add(rhodes(hz(m),1.6),23.35+0.05*k,0.03,pan=0.3-0.2*k)
# sidechain pump
pump=np.ones(N)
for i in range(int(22/B)):
    t=i*B
    if t>=3.0:
        a=int(t*SR); n=int(0.2*SR); pump[a:a+n]=np.minimum(pump[a:a+n],0.5+0.5*np.linspace(0,1,n)**0.6)
L*=pump; R*=pump
fo=np.ones(N); k=int(1.2*SR); fo[-k:]=np.linspace(1,0,k)**1.5; L*=fo; R*=fo
L=np.tanh(L*1.2); R=np.tanh(R*1.2)
m=max(abs(L).max(),abs(R).max()); L/=m*1.05; R/=m*1.05
w=wave.open(sys.argv[1],'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((np.stack([L,R],1)*32767).astype(np.int16).tobytes()); w.close()
