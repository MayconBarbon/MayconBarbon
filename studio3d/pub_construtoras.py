# Publica /construtoras como RASCUNHO: corpo HTML + shortcode do CF7 + tour 3D embutido
import pickle,json,re,os,sys
W=os.path.dirname(os.path.abspath(__file__)); B='https://videoimovel.com.br'; SITE='/home/user/MayconBarbon/videoimovel-site/'
ss=pickle.load(open(W+'/sess.pkl','rb')); mp=json.load(open(W+'/media_map.json')); st=json.load(open(W+'/studio3d.json'))
s=open(SITE+'construtoras/index.body.html').read()
tour=open('/home/user/MayconBarbon/studio3d/tour/tour.build.js').read()
assert '&&' not in tour and '</script' not in tour
s=s.replace('__TOUR__',tour)
seo_t=re.search(r'<title>(.*?)</title>',s).group(1); seo_d=re.search(r'<meta name="description" content="([^"]*)"',s).group(1)
for rel in sorted(set(re.findall(r'(assets/[\w/.-]+\.(?:webp|png|jpg|mp4))',s))):
    if rel in mp: continue
    fn=os.path.basename(rel); ct={'webp':'image/webp','jpg':'image/jpeg','png':'image/png','mp4':'video/mp4'}[fn.rsplit('.',1)[1]]
    r=ss.post(B+'/wp-json/wp/v2/media',data=open(SITE+rel,'rb').read(),headers={'Content-Type':ct,'Content-Disposition':f'attachment; filename="vi-{fn}"'},timeout=300)
    mp[rel]=r.json()['source_url']; print('up',rel,mp[rel]); json.dump(mp,open(W+'/media_map.json','w'),indent=1)
b=re.sub(r'<title>.*?</title>\n?','',s); b=re.sub(r'<meta [^>]*>\n?','',b)
for k,url in sorted(mp.items(),key=lambda x:-len(x[0])):
    if k.startswith('assets/'): b=b.replace(k,url)
left=re.findall(r'assets/[\w/.-]+\.(?:webp|png|jpg|mp4)',b); print('não mapeados',left)
a,c=b.split('<!--CF7-->')
content='<!-- wp:html -->\n'+a+'\n<!-- /wp:html -->\n<!-- wp:shortcode -->\n[contact-form-7 id="%d" html_class="vi3d-form"]\n<!-- /wp:shortcode -->\n<!-- wp:html -->\n'%st['cf7_id']+c+'\n<!-- /wp:html -->'
pid=st.get('page_id')
data={'title':'Studio 3D para construtoras','slug':'construtoras','status':os.environ.get('STATUS','draft'),'template':'elementor_canvas','content':content}
r=ss.post(B+'/wp-json/wp/v2/pages'+(f'/{pid}' if pid else ''),json=data,timeout=120); j=r.json(); print(r.status_code,j.get('id'),j.get('status'),j.get('link'))
st['page_id']=j['id']; json.dump(st,open(W+'/studio3d.json','w'))
r=ss.put(B+f'/wp-json/seopress/v1/posts/{j["id"]}/title-description-metas',json={'title':seo_t,'description':seo_d}); print('seo',r.status_code)
