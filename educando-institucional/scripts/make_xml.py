"""Build a Premiere-importable FCP7 XML (xmeml v4) from edl.json.
Media paths point to the user's local folders: <ROOT>/Dia 1|2|3/fx3 gabrielNNNN.MP4
usage: python3 make_xml.py edl.json out.xml"""
import json, sys, csv, os
from xml.sax.saxutils import escape
from urllib.parse import quote
S="/tmp/claude-0/-home-user-MayconBarbon/99707c74-1abd-56d4-a68a-c149be73686e/scratchpad"
edl=json.load(open(sys.argv[1])); out=sys.argv[2]
ROOT=edl.get("media_root","C:/Users/USUARIO/Google Drive/#2026/#Educando Institucional")
DAYDIR={"D1":"Dia 1","D2":"Dia 2","D3":"Dia 3"}
TB=30; NTSC="TRUE"  # 29.97
SRC_TB=60           # 59.94 source
def fr(sec,tb=TB): return int(round(sec*tb*1000/1001))
dur_src={}
for d in ("D1","D2","D3"):
    pass
def clip_dur(day,clip):
    p=f"{S}/proc/{day}/{clip}/probe.json"
    return float(json.load(open(p))["format"]["duration"]) if os.path.exists(p) else 60.0
def rate(tb): return f"<rate><timebase>{tb}</timebase><ntsc>{NTSC}</ntsc></rate>"
files={}; vitems=[]; aitems=[]; t=0
for i,sh in enumerate(edl["shots"]):
    d=sh["dur"]; st=fr(t); en=fr(t+d); t+=d
    if sh.get("type","clip")!="clip":
        vitems.append(f'<generatoritem id="gen{i}"><name>{escape(sh.get("label","Slug"))}</name>{rate(TB)}<start>{st}</start><end>{en}</end><in>0</in><out>{en-st}</out><effect><name>Slug</name><effectid>Slug</effectid><effectcategory>Matte</effectcategory><effecttype>generator</effecttype><mediatype>video</mediatype></effect></generatoritem>')
        continue
    day,clip=sh["day"],sh["clip"]; num=clip[1:]
    fid=f"file-{day}-{clip}"
    name=f"fx3 gabriel{num}.MP4"
    sp=sh.get("speed",1.0)
    # source in/out in sequence timebase frames (Premiere will conform); speed via timeremap
    sin=fr(sh["in"]); sout=sin+int(round((en-st)*sp))
    tot=fr(clip_dur(day,clip))
    if fid not in files:
        path=f"{ROOT}/{DAYDIR[day]}/{name}"
        url="file://localhost/"+quote(path.replace("\\","/"),safe="/:#")
        url=url.replace("#","%23")
        files[fid]=f'<file id="{fid}"><name>{name}</name><pathurl>{url}</pathurl>{rate(TB)}<duration>{tot}</duration><media><video><samplecharacteristics>{rate(TB)}<width>3840</width><height>2160</height></samplecharacteristics></video><audio><channelcount>2</channelcount></audio></media></file>'
        fxml=files[fid]
    else:
        fxml=f'<file id="{fid}"/>'
    speedfx=""
    if sp!=1.0:
        speedfx=f'<filter><effect><name>Time Remap</name><effectid>timeremap</effectid><effectcategory>motion</effectcategory><effecttype>motion</effecttype><mediatype>video</mediatype><parameter><parameterid>speed</parameterid><name>speed</name><value>{sp*100:.1f}</value></parameter><parameter><parameterid>variablespeed</parameterid><name>variablespeed</name><value>0</value></parameter></effect></filter>'
    scale='<filter><effect><name>Basic Motion</name><effectid>basic</effectid><effectcategory>motion</effectcategory><effecttype>motion</effecttype><mediatype>video</mediatype><parameter><parameterid>scale</parameterid><name>Scale</name><value>50</value></parameter></effect></filter>'
    lab=escape(f'{sh.get("block","")} {sh.get("note","")}'.strip())
    vitems.append(f'<clipitem id="v{i}"><name>{name}</name><duration>{tot}</duration>{rate(TB)}<start>{st}</start><end>{en}</end><in>{sin}</in><out>{sout}</out>{fxml}{scale}{speedfx}<comments><mastercomment1>{lab}</mastercomment1></comments></clipitem>')
    if sh.get("audio")!="mute":
        ain=fr(sh["in"]); aout=ain+(en-st)
        aitems.append(f'<clipitem id="a{i}"><name>{name}</name><duration>{tot}</duration>{rate(TB)}<start>{st}</start><end>{en}</end><in>{ain}</in><out>{aout}</out><file id="{fid}"/><sourcetrack><mediatype>audio</mediatype><trackindex>1</trackindex></sourcetrack><filter><effect><name>Audio Levels</name><effectid>audiolevels</effectid><effectcategory>audiolevels</effectcategory><effecttype>audiolevels</effecttype><mediatype>audio</mediatype><parameter><parameterid>level</parameterid><name>Level</name><value>{10**(sh.get("amb_db",-14)/20):.3f}</value></parameter></effect></filter></clipitem>')
TOTAL=fr(t)
def ext_audio(idx,path,start,d,name,db=0):
    st=fr(start); n=fr(d)
    url="file://localhost/"+quote(path,safe="/:")
    return f'<clipitem id="x{idx}"><name>{escape(name)}</name>{rate(TB)}<start>{st}</start><end>{st+n}</end><in>0</in><out>{n}</out><file id="xf{idx}"><name>{escape(name)}</name><pathurl>{url}</pathurl>{rate(TB)}<duration>{n}</duration><media><audio><channelcount>1</channelcount></audio></media></file><filter><effect><name>Audio Levels</name><effectid>audiolevels</effectid><effectcategory>audiolevels</effectcategory><effecttype>audiolevels</effecttype><mediatype>audio</mediatype><parameter><parameterid>level</parameterid><name>Level</name><value>{10**(db/20):.3f}</value></parameter></effect></filter></clipitem>'
vo=[]
for j,v in enumerate(edl.get("vo",[])):
    rel=f"{ROOT}/projeto/claude_montagem/locucao_guia/{os.path.basename(v['path'])}"
    dd=float(os.popen(f"ffprobe -v error -show_entries format=duration -of csv=p=0 '{v['path']}'").read())
    vo.append(ext_audio(j,rel,v["start"],dd,"GUIA "+os.path.basename(v["path"]),v.get("db",0)))
mus=[]
m=edl.get("music")
if m:
    rel=f"{ROOT}/projeto/claude_montagem/trilha/{os.path.basename(m['path'])}"
    mus.append(ext_audio(900,rel,m.get("start",0),TOTAL/ (30000/1001) - m.get("start",0),"TRILHA PROVISORIA "+os.path.basename(m["path"]),-12))
markers="".join(f'<marker><name>{escape(x["text"])}</name><comment>{escape(x.get("comment",""))}</comment><in>{fr(x["t"])}</in><out>-1</out></marker>' for x in edl.get("markers",[]))
def track(items): return "<track>"+"".join(items)+"</track>"
xml=f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE xmeml>
<xmeml version="4"><sequence id="seq1"><name>{escape(edl.get("title","Educando - O que pode existir depois daqui"))}</name><duration>{TOTAL}</duration>{rate(TB)}
<timecode>{rate(TB)}<string>00:00:00;00</string><frame>0</frame><displayformat>DF</displayformat></timecode>{markers}
<media><video><format><samplecharacteristics>{rate(TB)}<width>1920</width><height>1080</height><pixelaspectratio>square</pixelaspectratio><fielddominance>none</fielddominance></samplecharacteristics></format>
{track(vitems)}</video>
<audio>{track(aitems)}{track(vo)}{track(mus)}</audio></media></sequence></xmeml>'''
open(out,"w").write(xml)
print("xml", len(vitems), "video items", len(aitems), "amb", len(vo), "vo", TOTAL, "frames")
