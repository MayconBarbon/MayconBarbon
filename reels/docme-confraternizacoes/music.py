# Synth: 120 BPM, elegant disco/house, 25 s. Key: A minor -> C. Beat = 0.5 s; bar = 2 s.
import numpy as np, wave
SR=48000; BPM=120; B=60/BPM; DUR=25.0; N=int(SR*DUR)
t=np.arange(N)/SR; L=np.zeros(N); R=np.zeros(N)
rng=np.random.default_rng(7)
def add(sig,start,gain=1.0,pan=0.0):
    i=int(start*SR); j=min(N,i+len(sig))
    if j<=i: return
    s=sig[:j-i]*gain
    L[i:j]+=s*(1-pan)*0.5*2**0.5*0.71; R[i:j]+=s*(1+pan)*0.5*2**0.5*0.71
def env(n,a,d):
    e=np.ones(n); na=max(1,int(a*SR)); e[:na]=np.linspace(0,1,na); e*=np.exp(-np.arange(n)/SR/d); return e
def kick():
    n=int(0.45*SR); tt=np.arange(n)/SR; f=48+90*np.exp(-tt*28); ph=2*np.pi*np.cumsum(f)/SR
    return np.sin(ph)*np.exp(-tt*7)+0.15*np.sin(ph*2)*np.exp(-tt*30)
def clap():
    n=int(0.25*SR); x=rng.standard_normal(n); e=np.zeros(n)
    for k in (0,0.011,0.022): e+=np.exp(-np.clip(np.arange(n)/SR-k,0,None)*40)*(np.arange(n)/SR>=k)
    from numpy.fft import rfft,irfft
    X=rfft(x); fr=np.fft.rfftfreq(n,1/SR); X*=np.exp(-((fr-1500)/1200)**2); return irfft(X,n)*e*3
def hat(open_=False):
    n=int((0.18 if open_ else 0.05)*SR); x=rng.standard_normal(n); x=np.diff(np.concatenate([[0],x]))
    return x*np.exp(-np.arange(n)/SR*(14 if open_ else 70))*0.5
def note(f,dur,kind='pad'):
    n=int(dur*SR); tt=np.arange(n)/SR
    if kind=='pad':
        s=sum(np.sin(2*np.pi*f*d*tt+rng.uniform(0,6)) for d in (1,1.004,0.996))/3
        s+=0.3*sum(np.sin(2*np.pi*2*f*d*tt) for d in (1,1.003))/2
        e=np.minimum(1,tt/0.04)*np.minimum(1,(dur-tt)/0.08)
    elif kind=='bass':
        s=np.sin(2*np.pi*f*tt)+0.35*np.sin(4*np.pi*f*tt)+0.12*np.sign(np.sin(2*np.pi*f*tt))
        e=np.minimum(1,tt/0.005)*np.exp(-tt*3)*np.minimum(1,(dur-tt)/0.02)
    elif kind=='pluck':
        s=np.sin(2*np.pi*f*tt)+0.5*np.sin(4*np.pi*f*tt)*np.exp(-tt*12)+0.2*np.sin(6*np.pi*f*tt)*np.exp(-tt*20)
        e=np.exp(-tt*7)*np.minimum(1,tt/0.003)
    return s*e
def hz(m): return 440*2**((m-69)/12)
# chords per bar (2 s): Am7, Fmaj7, C, G  (midi)
prog=[[57,60,64,67],[53,57,60,64],[48,55,60,64],[55,59,62,67]]
roots=[45,41,48,43]
bars=int(np.ceil(DUR/2))
for b in range(bars):
    t0=b*2.0; c=prog[b%4]
    # sections: 0-3 intro (filtered-ish, no kick first bar half), drops at 3, 9, 18; outro 22-25 big then ring
    full = t0>=3.0 and t0<23.0
    for m in c:
        add(note(hz(m),2.0,'pad'),t0,0.05 if t0<3 else 0.07,pan=rng.uniform(-.4,.4))
    if t0>=1.0:
        for k in range(8):  # offbeat bass eighths
            tt=t0+k*B/2
            if k%2==1 or t0>=3: add(note(hz(roots[b%4]+(12 if k in (3,7) else 0)),B/2*0.9,'bass'),tt,0.22 if t0>=3 else 0.12)
    # plucks arpeggio 16ths
    if t0>=3.0:
        arp=[c[0]+12,c[1]+12,c[2]+12,c[3]+12,c[2]+12,c[1]+12,c[3]+12,c[2]+24]
        for k in range(16):
            add(note(hz(arp[k%8]),0.3,'pluck'),t0+k*B/4,0.045,pan=(-0.5 if k%2 else 0.5))
# drums
for i in range(int(DUR/B)):
    tb=i*B
    if tb>=23.0: break
    if tb>=3.0 or (tb>=1.0 and i%2==0): add(kick(),tb,0.55)
    if tb>=3.0 and i%2==1: add(clap(),tb,0.20)
    if tb>=2.0: add(hat(True),tb+B/2,0.10); add(hat(),tb+B/4,0.05); add(hat(),tb+3*B/4,0.05)
# riser before 3 s and 18 s; impact at 3, 9, 18, 22
def riser(d):
    n=int(d*SR); x=rng.standard_normal(n); tt=np.arange(n)/SR; return x*(tt/d)**2*0.25
for tr in (3.0,9.0,18.0,22.0): add(riser(1.0),tr-1.0,0.6)
def boom():
    n=int(1.6*SR); tt=np.arange(n)/SR; return np.sin(2*np.pi*(40+40*np.exp(-tt*8))*tt)*np.exp(-tt*2.5)
for tr in (3.0,9.0,18.0,22.0): add(boom(),tr,0.5)
# final chord ring
for m in [48,55,60,64,67,72]: add(note(hz(m),3.0,'pad'),22.0,0.08)
# sidechain pump
pump=np.ones(N)
for i in range(int(DUR/B)):
    tb=i*B
    if 3.0<=tb<23.0:
        a=int(tb*SR); n=int(0.25*SR); pump[a:a+n]=np.minimum(pump[a:a+n],0.45+0.55*np.linspace(0,1,n)**0.6)
L*=pump; R*=pump
# fade out last 1.2 s
fo=np.ones(N); k=int(1.2*SR); fo[-k:]=np.linspace(1,0,k)**1.5; L*=fo; R*=fo
m=max(np.abs(L).max(),np.abs(R).max()); L/=m*1.1; R/=m*1.1
st=(np.stack([L,R],1)*32767).astype(np.int16)
w=wave.open(__import__('sys').argv[1],'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(st.tobytes()); w.close()
