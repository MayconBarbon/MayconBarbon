"""5 anúncios de 15 s (dor → solução → convite), estilo da VSL v3, voz do Gabriel.
Política de anúncios Meta: sem promessa de ganho, sem valores de renda, sem situação pessoal do leitor."""
import json, re, subprocess, os, sys
FINAL = dict(tipo="FINAL", flash=0.6, ctaMd="Conheça os **materiais.**", fala="[warmly] Storymaker Oficial. Conheça os materiais.")
ADS = {
 "01-o-que-gravar": [
   dict(tipo="FOOT", lay="S", clips=[(4632, 1), (51540, 2), (4385, 2)], tituloMd="O que gravar **primeiro?**", fala="[curious] Chegou no evento e não sabe o que gravar primeiro?"),
   dict(tipo="WHEEL", tituloMd="**Checklist** de cobertura", wl="comece", itens=["pelos primeiros 15 min", "pelo lugar", "pelas pessoas", "pelas atrações", "pelo encerramento"], fala="O Checklist de cobertura mostra os primeiros quinze minutos e a sequência que conta a história."),
   FINAL],
 "02-imagens-sem-historia": [
   dict(tipo="FOOT", lay="S", clips=[(5224, 0.5), (51553, 1), (1187, 1)], tituloMd="Bonito, mas **sem história?**", fala="Imagens bonitas, mas sem história?"),
   dict(tipo="FOOT", lay="S", clips=[(5217, 0.5), (5206, 1), (18204, 4)], tituloMd="", rotulos=["ABERTO", "MÉDIO", "DETALHE"], fala="Alterne plano aberto, médio e detalhe. O e-book Do briefing à história ensina a sequência."),
   FINAL],
 "03-o-que-o-cliente-espera": [
   dict(tipo="FOOT", lay="S", clips=[(41222, 1), (43256, 0.5), (4537, 3)], tituloMd="O que o cliente **espera?**", fala="Você não sabe o que o cliente espera de verdade?"),
   dict(tipo="SWAP", rotulo="Modelo de briefing", frases=["Qual é o **objetivo?**", "Quem precisa **aparecer?**", "O que não pode **faltar?**"], fala="O Modelo de briefing conduz a conversa com o cliente, pergunta por pergunta."),
   FINAL],
 "04-o-momento-que-nao-volta": [
   dict(tipo="FOOT", lay="S", clips=[(51529, 1), (51643, 2), (4632, 4)], tituloMd="O momento que não **volta**", fala="[pause] Medo de perder a fala, a entrada ou o brinde?"),
   dict(tipo="LIST", lt="Áudio e pessoas", ll="antes", itens=["lista A/B/C", "fonte principal", "áudio de backup", "teste de som", "cópia de segurança"], fala="Com a lista de pessoas e o Checklist de áudio, você chega pronto para o que não se repete."),
   FINAL],
 "05-orcamento-completo": [
   dict(tipo="FOOT", lay="S", clips=[(44071, 2), (4919, 1), (1780, 2)], tituloMd="Seu orçamento conta **tudo?**", fala="Seu orçamento conta a reunião, o deslocamento e a edição?"),
   dict(tipo="LIST", lt="Planilha de custos", ll="horas", itens=["reunião de briefing", "pesquisa do cliente", "deslocamento", "horas no evento", "edição e entrega"], fala="A Planilha de custos e horas soma cada etapa, para você cobrar com método."),
   FINAL],
}
VOZ, MOD = "WPgqgCVa3mD38JuyODU6", "eleven_v4"
FON = [(r"\bKiwify\b", "Kiuí-fai")]
LIMPA = lambda t: re.sub(r"\[[a-z ]+\]\s*", "", t).strip()
def sh(*a, **k): return subprocess.run(list(a), capture_output=True, text=True, **k)
def chunks(texto, n=4):
    out = []
    for frase in [f.strip() for f in re.split(r"(?<=[,:.?!])\s+", texto) if f.strip()]:
        w = frase.split()
        while w:
            k = n if len(w) != n + 1 else n + 1
            out.append(" ".join(w[:k])); w = w[k:]
    res = []
    for x in out:
        if res and len(x.split()) == 1 and len(res[-1].split()) < 5: res[-1] += " " + x
        else: res.append(x)
    return res
def destaque(ch):
    ws = [re.sub(r"[^\wÀ-ú/-]", "", x) for x in ch.split()]; i = max(range(len(ws)), key=lambda j: len(ws[j])); return i if len(ws[i]) > 3 else -1

so = sys.argv[1:] or list(ADS)
os.makedirs("ads", exist_ok=True); relatorio = []
for nome in so:
    D = f"ads/{nome}"; os.makedirs(D, exist_ok=True); cenas = []; t0 = 0.0
    for n, e in enumerate(ADS[nome], 1):
        e = json.loads(json.dumps(e))
        txt = e["fala"]
        for a, b in FON: txt = re.sub(a, b, txt)
        mp3 = f"{D}/g{n}.mp3"
        if not os.path.exists(mp3):
            r = sh("curl", "-sS", "-X", "POST", f"https://api.elevenlabs.io/v1/text-to-speech/{VOZ}?output_format=mp3_44100_128", "-H", "xi-api-key: proxy-injected",
                   "-H", "Content-Type: application/json", "-d", json.dumps({"text": txt, "model_id": MOD, "language_code": "pt"}), "-o", mp3, "-w", "%{http_code}")
            assert r.stdout == "200", (nome, n, r.stdout)
        dv = float(sh("ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", mp3).stdout)
        tr = json.loads(sh("curl", "-sS", "-X", "POST", "https://api.elevenlabs.io/v1/speech-to-text", "-H", "xi-api-key: proxy-injected", "-F", "model_id=scribe_v1", "-F", f"file=@{mp3}").stdout).get("text", "")
        pad_ini, pad_fim = (0.15, 0.2) if e["tipo"] != "FINAL" else (0.55, 0.45)
        dur = round(pad_ini + dv + pad_fim, 2)
        legs = chunks(LIMPA(e["fala"])); pesos = [len(x.split()) + 0.6 for x in legs]; tot = sum(pesos); t = pad_ini; L = []
        for x, p in zip(legs, pesos):
            dd = dv * p / tot; L.append({"texto": x, "ini": round(t, 2), "fim": round(t + dd, 2), "hl": destaque(x)}); t += dd
        L[-1]["fim"] = round(dur - 0.05, 2)
        tf = round(min(1.6, max(1.1, dur * 0.35)), 2) if e.get("tituloMd") and e["tipo"] == "FOOT" else 0
        if tf:
            for x in L: x["ini"] = max(x["ini"], tf)
            L = [x for x in L if x["fim"] - x["ini"] > 0.3]
        cenas.append({**e, "n": n, "dur": dur, "inicio": round(t0, 2), "pad_ini": pad_ini, "voz": mp3, "voz_dur": dv, "caps": L, "titulo_fim": tf, "transcricao": tr})
        t0 += dur
    json.dump(cenas, open(f"{D}/plano.json", "w"), ensure_ascii=False, indent=1)
    subprocess.run(["node", "ads_render.js"], env={**os.environ, "PLANO": f"{D}/plano.json", "OUT": D}, check=True, capture_output=True)
    lista = []
    for c in cenas:
        n, d = c["n"], c["dur"]; out = f"{D}/s{n}.mp4"; seq = f"{D}/f{n:02d}/%05d.png"
        if c["tipo"] != "FOOT":
            cmd = ["-framerate", "30", "-i", seq, "-filter_complex", "[0:v]format=yuv420p[out]"]
        else:
            ins, fc = [], [f"color=c=0x1b1a1f:s=1080x1920:r=30:d={d}[base]"]; cur = "base"
            for k, (clip, ss) in enumerate(c["clips"]):
                ins += ["-stream_loop", "-1", "-ss", str(ss), "-t", str(d + 0.5), "-i", f"clips/{clip}.mp4"]
                z = f"(1+0.08*t/{d})"
                if c["lay"] == "V":
                    fc.append(f"[{k}:v]fps=30,scale=w='ceil(1080*{z}/2)*2':h=-2:eval=frame,crop=1080:1920,setsar=1[t{k}]"); fc.append(f"[{cur}][t{k}]overlay=0:0:shortest=1[c{k}]")
                else:
                    y = [32, 656, 1280][k]; dl = 0.07 * k; s = -1 if k % 2 == 0 else 1
                    fc.append(f"[{k}:v]fps=30,scale=w='ceil(1080*{z}/2)*2':h=-2:eval=frame,crop=1080:608,setsar=1[t{k}]")
                    fc.append(f"[{cur}][t{k}]overlay=x='{s}*1080*(1-min(1,max(0,(t-{dl})/0.25))^0.35)':y={y}:shortest=1[c{k}]")
                cur = f"c{k}"
            m = len(c["clips"]); ins += ["-framerate", "30", "-i", seq]
            fc.append(f"[{cur}]trim=0:{d},setpts=PTS-STARTPTS[bb];[{m}:v]format=rgba[ov];[bb][ov]overlay=0:0:shortest=1,format=yuv420p[out]")
            cmd = ins + ["-filter_complex", ";".join(fc)]
        r = sh("ffmpeg", "-v", "error", "-y", *cmd, "-map", "[out]", "-t", str(d), "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-r", "30", "-pix_fmt", "yuv420p", out)
        if r.returncode: print(r.stderr[-1000:]); raise SystemExit(1)
        lista.append(f"file 's{n}.mp4'")
    open(f"{D}/lista.txt", "w").write("\n".join(lista) + "\n")
    sh("ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{D}/lista.txt", "-c", "copy", f"{D}/sem_som.mp4")
    Dur = float(sh("ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"{D}/sem_som.mp4").stdout)
    al = []
    for c in cenas:
        o = f"{D}/a{c['n']}.wav"; sh("ffmpeg", "-v", "error", "-y", "-i", c["voz"], "-af", f"adelay={int(c['pad_ini']*1000)},apad,atrim=0:{c['dur']}", "-ar", "48000", "-ac", "1", o); al.append(f"file 'a{c['n']}.wav'")
    open(f"{D}/lista_a.txt", "w").write("\n".join(al) + "\n")
    sh("ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{D}/lista_a.txt", "-c", "pcm_s16le", f"{D}/voz.wav")
    r = sh("ffmpeg", "-v", "error", "-y", "-i", f"{D}/sem_som.mp4", "-i", f"{D}/voz.wav", "-ss", "50", "-i", "m634.mp3", "-filter_complex",
           f"[1:a]loudnorm=I=-16:TP=-1.5:LRA=11,aformat=channel_layouts=stereo[v];[2:a]atrim=0:{Dur},afade=t=in:d=0.4,afade=t=out:st={Dur-1.5:.2f}:d=1.5,volume=0.16[m];[v][m]amix=inputs=2:duration=first:normalize=0[a]",
           "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-t", str(Dur), "-movflags", "+faststart", f"ads/anuncio-{nome}-15s.mp4")
    if r.returncode: print(r.stderr[-800:]); raise SystemExit(1)
    relatorio.append({"anuncio": nome, "duracao": round(Dur, 2), "falas": [(c["fala"], c["transcricao"]) for c in cenas]})
    print(nome, round(Dur, 2), "s |", " / ".join(c["transcricao"] for c in cenas), flush=True)
json.dump(relatorio, open("ads/relatorio.json", "w"), ensure_ascii=False, indent=1)
