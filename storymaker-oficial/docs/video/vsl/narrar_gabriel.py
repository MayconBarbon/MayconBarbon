"""Narração com a voz fixa da marca: Gabriel — Friendly Brazilian Ad Voice (ElevenLabs).
A chave é injetada pelo proxy da sessão (cabeçalho xi-api-key); nada fica salvo no código."""
import json, re, subprocess
VOZ, MODELO = "WPgqgCVa3mD38JuyODU6", "eleven_v4"
FONETICA = [(r"\bDocMe\b", "Dóc Mi"), (r"\bKiwify\b", "Kiuí-fai")]
cenas = json.load(open("cenas.json")); t = 0.0
for c in cenas:
    txt = c["fala"]
    for a, b in FONETICA: txt = re.sub(a, b, txt)
    mp3 = f"gabriel/g{c['n']:02d}.mp3"
    body = json.dumps({"text": txt, "model_id": MODELO, "language_code": "pt"})
    r = subprocess.run(["curl", "-sS", "-X", "POST", f"https://api.elevenlabs.io/v1/text-to-speech/{VOZ}?output_format=mp3_44100_128",
                        "-H", "xi-api-key: proxy-injected", "-H", "Content-Type: application/json", "-d", body, "-o", mp3, "-w", "%{http_code}"], capture_output=True, text=True)
    assert r.stdout == "200", (c["n"], r.stdout, open(mp3, errors="ignore").read()[:300])
    dv = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", mp3], capture_output=True, text=True).stdout)
    pad_ini, pad_fim = 0.25, (2.4 if c["clip"] is None else 0.35)
    c.update({"voz": mp3, "voz_dur": round(dv, 2), "pad_ini": pad_ini, "dur": round(pad_ini + dv + pad_fim, 2), "inicio": round(t, 2)})
    t += c["dur"]
    stt = subprocess.run(["curl", "-sS", "-X", "POST", "https://api.elevenlabs.io/v1/speech-to-text", "-H", "xi-api-key: proxy-injected", "-F", "model_id=scribe_v1", "-F", f"file=@{mp3}"], capture_output=True, text=True).stdout
    c["transcricao"] = json.loads(stt).get("text", "")
    print(c["n"], f"{dv:.1f}s |", c["transcricao"], flush=True)
json.dump(cenas, open("cenas.json", "w"), ensure_ascii=False, indent=1)
print(f"total {t:.1f}s")
