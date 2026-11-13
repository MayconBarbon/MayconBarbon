import sys, os, json, glob, wave
import numpy as np
from faster_whisper import WhisperModel
S = "/tmp/claude-0/-home-user-MayconBarbon/99707c74-1abd-56d4-a68a-c149be73686e/scratchpad"
model = WhisperModel(sys.argv[1] if len(sys.argv) > 1 else "small", device="cpu", compute_type="int8", cpu_threads=2)
for d in sorted(glob.glob(f"{S}/proc/D*/C*")):
    if not os.path.exists(f"{d}/done") or os.path.exists(f"{d}/transcript.json"):
        continue
    w = wave.open(f"{d}/audio16k.wav"); a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
    segs, info = model.transcribe(a, language="pt", vad_filter=True, beam_size=1)
    out = [{"s": round(s.start, 2), "e": round(s.end, 2), "t": s.text.strip(), "p": round(s.avg_logprob, 2), "ns": round(s.no_speech_prob, 2)} for s in segs]
    json.dump(out, open(f"{d}/transcript.json", "w"), ensure_ascii=False)
    print(d.split("/")[-2] + "/" + d.split("/")[-1], len(out), " | ".join(x["t"] for x in out)[:200], flush=True)
