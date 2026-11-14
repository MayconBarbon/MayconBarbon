"""Corte 1 EDL — follows script blocks/timings. Gaps = labelled black slugs."""
import json, csv
S="/tmp/claude-0/-home-user-MayconBarbon/99707c74-1abd-56d4-a68a-c149be73686e/scratchpad"
cat={}
for d in ("D1","D2"):
    for r in csv.reader(open(f"{S}/catalog_{d}.tsv"),delimiter="\t"):
        cat[r[0]]=(d,r)
def bw(c):
    a,b=cat[c][1][6].split("-"); return float(a),float(b)
MUTE={f"C06{n:02d}" for n in range(5,15)}  # takes dirigidos (voz da direção no áudio)
shots=[]; texts=[]; vo=[]; markers=[]; table=[]
t=0.0
def clip(block,c,dur,off=0.0,speed=1.0,note="",scene=""):
    global t
    d,_=cat[c]; a,b=bw(c); i=min(a+off, max(a,b-dur*speed))
    sid=f"s{len(shots):03d}"
    shots.append(dict(id=sid,type="clip",day=d,clip=c,**{"in":round(i,2)},dur=dur,speed=speed,block=block,
        audio="mute" if c in MUTE else "amb",amb_db=-90 if c in MUTE else -18,note=note))
    if note: texts.append(dict(start=t+0.1,end=t+dur-0.1,text=note,style="Note",fade=0.1))
    table.append((block,scene,f"fx3 gabriel{c[1:]}.MP4 ({'Dia 1 – 27.08' if d=='D1' else 'Dia 2 – 08.09'}) {i:.1f}s+{dur*speed:.1f}s","Material bruto do Instituto","PROVISÓRIO – substituir" if note else "Utilizado"))
    t+=dur
def gap(block,label,dur,scene=None):
    global t
    sid=f"s{len(shots):03d}"
    shots.append(dict(id=sid,type="black",dur=dur,block=block,label=label))
    texts.append(dict(start=t+0.05,end=t+dur-0.05,text="LACUNA · "+label,style="Gap",fade=0.15))
    markers.append(dict(t=t,dur=dur,name="LACUNA: "+label))
    table.append((block,scene or label,"—","—","PENDENTE (material não encontrado)"))
    t+=dur
def V(k,at,db=0): vo.append(dict(path=f"{S}/tts/vo/{k}.wav",start=at,db=db,key=k))
def T(a,b,txt,style="Sub",fade=0.6,pos=""): texts.append(dict(start=a,end=b,text=txt,style=style,fade=fade,pos=pos))
def DEP(a,b,txt):
    texts.append(dict(start=a,end=b,text="ÁUDIO DE ARQUIVO PENDENTE\\N«"+txt+"»",style="Dep",fade=0.2)); markers.append(dict(t=a,dur=b-a,name="DEPOIMENTO PENDENTE: "+txt))
    table.append((cur,"Áudio real: «"+txt+"»","—","—","PENDENTE (depoimento não encontrado)"))
# ---------- B1 0:00–0:25
cur=B="B1 0:00–0:25 Todo dia, alguém entra"
shots.append(dict(id="s000",type="black",dur=1.5,block=B)); t=1.5
table.append((B,"Tela preta + som direto","—","—","Utilizado (som ambiente do portão)"))
clip(B,"C0607",3.0,scene="P01 portão sendo aberto")
clip(B,"C0609",2.5,off=3,scene="P02 pés/mochila entrando")
clip(B,"C0605",2.5,off=2,scene="P03 criança atravessando o Instituto")
clip(B,"C0610",2.5,off=4,scene="P03 campo + prédio ao fundo")
clip(B,"C0611",2.5,scene="P04 educador cumprimenta a criança")
clip(B,"C0629",2.0,off=4,scene="P05 encontro com outras crianças")
gap(B,"P06 TEATRO (ação teatral real)",2.0)
clip(B,"C0645",1.5,scene="P07 MÚSICA mão no instrumento")
clip(B,"C1734",1.5,scene="P08 DIGITAL tela")
gap(B,"P09 FLAG presa à cintura",1.5)
clip(B,"C0668",2.0,off=2,scene="P10 FUTEBOL chuteira amarrada")
V("B1_01",3.2); V("B1_02",9.5)
# ---------- B2 0:25–0:55
cur=B="B2 0:25–0:55 Uma segunda casa"
clip(B,"C0612",3.0,scene="Criança-personagem encontra educadora")
clip(B,"C0615",3.0,scene="Encontra amigos / chegada")
clip(B,"C0659",3.0,off=3,scene="FUTEBOL professor explicando")
clip(B,"C0651",3.5,off=6,scene="MÚSICA professor demonstrando")
gap(B,"TEATRO infantil (expressão, interação, riso)",3.0)
clip(B,"C0667",2.5,off=4,scene="FUTEBOL chuteira sendo amarrada")
clip(B,"C0671",2.5,off=3,scene="FUTEBOL bola rolando / tentativa")
gap(B,"FLAG infantil (flag na cintura, corrida, retirada)",2.5)
clip(B,"C0638",3.0,off=6,scene="MÚSICA concentração / amizade")
clip(B,"C0684",4.0,off=10,scene="Convivência (risada espontânea)")
V("B2_01",26.0); V("B2_02",29.6); V("B2_03",32.2); V("B2_04",34.6)
DEP(40.0,52.0,"Aqui foi a nossa segunda casa. A gente aprendeu com as amizades, com os professores, a ser pessoas melhores...")
# ---------- B3 0:55–1:20
cur=B="B3 0:55–1:20 De onde viemos"
gap(B,"ARQUIVO 1997: campo, primeiros times",4.0)
clip(B,"C0657",4.0,off=4,scene="Match cut → campo atual")
gap(B,"ARQUIVO: uniformes antigos / campeonatos",3.5)
clip(B,"C0662",4.0,off=5,scene="Match cut → time atual")
gap(B,"ARQUIVO: comunidade / famílias / grupo antigo",3.5)
clip(B,"C0628",3.0,off=3,scene="Match cut → grupo atual")
clip(B,"C0670",3.0,off=8,scene="Futebol atual (história maior que o campo)")
V("B3_01",56.0); V("B3_02",59.4); V("B3_03",66.8); V("B3_04",68.8); V("B3_05",71.0); V("B3_06",74.6)
# ---------- B4 1:20–1:55
cur=B="B4 1:20–1:55 Quando as possibilidades crescem"
clip(B,"C1742",2.5,off=3,scene="MÍDIAS DIGITAIS professor orientando")
clip(B,"C1728",2.5,off=4,scene="MÍDIAS DIGITAIS tela / por cima do ombro")
clip(B,"C1749",2.0,off=2,scene="MÍDIAS DIGITAIS mãos operando")
clip(B,"C1760",2.0,off=1,scene="MÍDIAS DIGITAIS resultado na tela")
clip(B,"C1671",2.0,off=3,scene="TÊNIS DE MESA raquetes")
clip(B,"C1695",2.0,scene="TÊNIS DE MESA saque")
clip(B,"C1686",1.5,off=2,scene="TÊNIS DE MESA bolinha cruza o quadro")
clip(B,"C0665",1.5,scene="→ FUTEBOL bola cruzando o quadro")
clip(B,"C0659",2.0,off=10,scene="FUTEBOL orientação / escuta")
clip(B,"C0660",2.0,off=3,scene="FUTEBOL plano baixo / pés")
gap(B,"TEATRO infantil (palco, corpo, interação)",3.0)
clip(B,"C0641",2.5,off=6,scene="MÚSICA instrumento")
clip(B,"C0652",2.5,off=8,scene="MÚSICA grupo")
gap(B,"FLAG infantil (preparação, corrida, flag retirada)",3.0)
clip(B,"C1786",2.5,scene="TÊNIS DE MESA professor corrige pegada")
clip(B,"C1700",1.5,off=2,scene="TÊNIS DE MESA rosto")
V("B4_01",81.0); V("B4_02",84.4); V("B4_03",91.6); V("B4_04",96.2)
T(103.5,112.5,"Futebol · Teatro · Música · Flag\\NMídias Digitais · Tênis de Mesa","Sub",0.6)
# ---------- B5 1:55–2:25
cur=B="B5 1:55–2:25 Adolescer também é descobrir"
gap(B,"MÍDIAS DIGITAIS adolescentes",7.0)
gap(B,"TEATRO adolescentes (obrigatório)",8.0)
gap(B,"MÚSICA adolescentes",7.0)
gap(B,"FUTEBOL adolescentes",8.0)
T(116,126,"PERGUNTA (condutor) PENDENTE\\N«Quando você encontra hoje um adulto que passou pelo Educando quando criança, o que espera perceber nele?»","Dep",0.2)
markers.append(dict(t=116,dur=10,name="PERGUNTA CONDUTOR PENDENTE"))
table.append((B,"Áudio pergunta do condutor","—","—","PENDENTE (áudio não encontrado)"))
DEP(128.0,136.0,"Era meio rebelde, o Ivan me colocava nos eixos.")
# ---------- B6 2:25–2:50
cur=B="B6 2:25–2:50 Aprender também é competir"
P="PROVISÓRIO: treino infantil — substituir por competitivo"
clip(B,"C0670",3.5,off=14,note=P,scene="FUTEBOL SUB-09")
clip(B,"C0671",3.0,off=10,note=P,scene="FUTEBOL SUB-11")
clip(B,"C0673",3.0,note=P,scene="FUTEBOL SUB-11 disputa")
clip(B,"C0674",3.0,off=12,note=P,scene="FUTEBOL SUB-15")
clip(B,"C0675",3.0,off=3,note=P,scene="FUTEBOL SUB-15 intensidade")
clip(B,"C0672",3.0,off=4,note=P,scene="FUTEBOL SUB-17")
gap(B,"FUTEBOL SUB-17 (atletas maduros, treinador)",2.5)
gap(B,"FLAG COMPETITIVO",4.0)
V("B6_01",146.0); V("B6_02",149.6); V("B6_03",152.0); V("B6_04",153.8); V("B6_05",155.6); V("B6_06",157.4); V("B6_07",159.0); V("B6_08",161.0)
T(163.5,169.5,"Sub-09 · Sub-11 · Sub-15 · Sub-17\\NFlag Competitivo","Sub",0.6)
# ---------- B7 2:50–3:10 (roteiro: 2:48–3:10)
cur=B="B7 2:50–3:10 Aprender não tem idade"
clip(B,"C0624",3.0,scene="VIOLÃO inserto (instrumentos da sala)")
gap(B,"VIOLÃO 50+ (mãos, cordas, sorriso ao conseguir)",7.0)
clip(B,"C1777",3.0,note="PROVISÓRIO: inserto de mouse — substituir por 50+",scene="INFORMÁTICA mouse/tela")
gap(B,"INFORMÁTICA 50+ (tentativa, colega ajudando, resultado)",7.0)
V("B7_01",171.0); V("B7_02",176.6)
T(172.0,178.0,"50+","Big",0.8)
# ---------- B8 3:10–3:35 (roteiro: 3:08–3:35)
cur=B="B8 3:10–3:35 As crianças de ontem"
gap(B,"TIAGO caminhando pelo Instituto",6.0)
gap(B,"CRIS observando atividade",6.0)
gap(B,"IVAN/Guardinha entre as crianças",6.0)
gap(B,"ARQUIVO foto antiga → rosto atual → criança atual",7.0)
for a,b,q in [(190.5,196.5,"TIAGO — Quando você olha para essas crianças, o que reconhece de você aqui?"),
              (197,203,"CRIS — Quando uma criança sair definitivamente daqui e seguir a vida dela, o que você espera que ela leve?"),
              (203.5,209.5,"IVAN — Depois de tantos anos, o que faz você continuar aqui?")]:
    T(a,b,"ENTREVISTA PENDENTE\\N«"+q+"»","Dep",0.2); markers.append(dict(t=a,dur=b-a,name="ENTREVISTA PENDENTE: "+q[:40]))
    table.append((B,"Entrevista: "+q.split(" —")[0],"—","—","PENDENTE (entrevista não encontrada)"))
# ---------- B9 3:35–3:55
cur=B="B9 3:35–3:55 O futuro não está escrito"
clip(B,"C0638",1.5,off=14,scene="Montagem final: criança tocando")
clip(B,"C1779",1.5,off=5,scene="Montagem: diante da tela")
gap(B,"50+ aprendendo",1.2)
clip(B,"C0671",1.5,off=18,scene="Montagem: correndo")
gap(B,"TEATRO",1.2)
clip(B,"C1812",1.5,off=4,scene="Montagem: tênis de mesa")
clip(B,"C0645",1.5,off=3,scene="Montagem: música")
gap(B,"FLAG",1.1)
clip(B,"C1724",1.5,off=15,scene="Montagem: educador orientando")
gap(B,"IVAN / CRIS / TIAGO + arquivo",1.5)
clip(B,"C0614",6.0,off=1,speed=0.5,scene="Criança-personagem volta (close)")
V("B9_01",216.0); V("B9_02",220.6); V("B9_03",225.8); V("B9_04",229.2)
# ---------- B10 3:55–4:15
cur=B="B10 3:55–4:15 O que pode existir depois daqui?"
clip(B,"C0613",4.0,off=4,scene="Criança encerra o dia, caminha (PROVISÓRIO: saída não filmada)",note="PROVISÓRIO: chegada usada como saída")
gap(B,"Adulto ex-integrante divide o quadro com a criança",3.0)
clip(B,"C0608",3.0,off=8,scene="Criança atravessa o portão")
clip(B,"C0650",1.5,off=2,scene="Rosto: criança")
gap(B,"Rostos: adolescente / 50+ / ex-integrante",1.5)
clip(B,"C1724",1.5,off=25,scene="Rosto: educador")
clip(B,"C0657",2.5,off=12,scene="Último plano: Instituto vivo (plano geral)")
shots.append(dict(id=f"s{len(shots):03d}",type="black",dur=3.0,block=B)); 
table.append((B,"Tela final","—","—","Utilizado (gerada)")); t+=3.0
V("B10_01",236.0); V("B10_02",240.8); V("B10_03",245.6)
DEP(248.6,251.0,"Você pode chegar onde você nem imagina.")
T(252.0,254.6,"INSTITUTO EDUCANDO PELO ESPORTE","Title",0.6,"{\\pos(960,500)}")
T(252.3,254.6,"O QUE PODE EXISTIR DEPOIS DAQUI?","Sub",0.6,"{\\pos(960,590)}")
print("total",round(t,2))
edl=dict(shots=shots,texts=texts,vo=vo,markers=markers,
  music=dict(path=f"{S}/music/bed_dreamer.wav",start=19.0,src_in=0,keys=[[19,-38],[25,-22],[110,-21],[115,-19],[145,-15],[168,-15],[171,-25],[190,-22],[215,-17],[247,-17],[255,-45]]),
  watermark="OFFLINE · baixa resolução · LOCUÇÃO-GUIA SINTÉTICA (gravação definitiva pendente) · trilha provisória",
  fade_in=0,fade_out=1.2,crf=22)
json.dump(edl,open(f"{S}/edl/corte1.json","w"),ensure_ascii=False,indent=1)
with open(f"{S}/edl/relatorio.tsv","w") as f:
    f.write("Bloco\tCena solicitada\tArquivo utilizado\tOrigem\tSituação\n")
    for r in table: f.write("\t".join(r)+"\n")
