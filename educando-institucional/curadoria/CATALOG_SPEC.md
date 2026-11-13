# Catalog spec — Instituto Educando pelo Esporte footage

Each clip folder: $S/proc/<DAY>/<CLIP>/ contains
- sheet.jpg  (6 evenly spaced keyframes)
- kf/NNNN.jpg (keyframes, ~1 per second: kf/0001 ≈ 0s, kf/0011 ≈ 10s; exact pts not stored — treat index-1 as seconds, approx)
- probe.json (duration in .format.duration; video 3840x2160 HEVC 59.94p)
- audio16k.wav, loud.txt (EBU R128 summary, "I:" integrated loudness)
Mosaics (8 clips per image, labeled with clip name + duration): $S/mosaic/<DAY>/m_*.jpg

Write ONE line per clip (TSV, no header) to $S/catalog_<DAY>.tsv with columns:
1 clip (e.g. C0605)
2 duration_s (integer)
3 tags — comma list from this fixed vocabulary only:
   PORTAO, CHEGADA, SAIDA, PERSONAGEM (the recurring girl with blue uniform + backpack), EDUCADOR, CONVIVENCIA, REFEITORIO,
   TEATRO, MUSICA, DIGITAL, FLAG, FUTEBOL, TENIS_MESA, VIOLAO, INFORMATICA, ENTREVISTA, FOTO_ANTIGA, COMPETITIVO,
   FACHADA_LOGO, PLANO_GERAL, DETALHE, ROSTO, CAMPO, OUTRO
4 ages — comma list of: crianca, adolescente, adulto, 50+
5 shot — geral / medio / close / detalhe / misto ; plus movement if obvious (fixo, movimento)
6 quality 1–5 (focus, exposure, framing, usable for a cinematic institutional film; 5 = hero shot)
7 best_window — best usable seconds as "a-b" (approx, from keyframe indices)
8 description in Portuguese, 1–2 sentences, concrete (who, what action, where). Mention emotion/spontaneity, logos, uniforms with age-group text (e.g. "Sub-15") if legible, sport score boards, stage/curtain, instruments, screens.

Rules: LOOK at the images (mosaics first; open sheet.jpg or kf/*.jpg for detail when unsure, e.g. to tell theater vs. dance, adolescents vs. kids, 50+). Do not guess from file names. Do not modify anything outside your catalog file and notes. Be honest when unclear ("indefinido").
