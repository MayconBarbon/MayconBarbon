// Imagens comparativas (mesmo enquadramento) e capas dos cards, sem textos sobrepostos
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
const OUT=path.join(__dirname,'stills');fs.mkdirSync(OUT,{recursive:true});
(async()=>{
 const b=await chromium.launch({args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--allow-file-access-from-files']});
 async function page(W,H){const p=await b.newPage({viewport:{width:W,height:H}});await p.goto('file://'+__dirname+'/film.html');
  await p.waitForFunction('window.FILM && window.RENDER');await p.evaluate(()=>FILM.ready);await p.addStyleTag({content:'.ov{display:none!important}'});return p;}
 // 1) comparativo: 5 estágios, mesma câmera
 const p=await page(1600,1000);
 const cam={p:[11.6,15.8,13.9],l:[4.45,0.0,3.9],fov:33};
 const st={
  '0-planta':{light:'studio',bg:'dark',plan:1,rise:0},
  '1-essencial':{light:'studio',bg:'dark',rise:1},
  '2-acabamentos':{light:'day',bg:'dark',rise:1,finishFloor:1,finishWall:1,basic:1},
  '3-decorado':{light:'afternoon',bg:'dark',rise:1,finishFloor:1,finishWall:1,basic:1,decor:1,lampsOn:0.2},
  '4-cinematic':{light:'dusk',bg:'sky',rise:1,finishFloor:1,finishWall:1,basic:1,decor:1,lampsOn:1,exposure:1.15}};
 for(const [k,s] of Object.entries(st)){await p.evaluate(([s,c])=>{FILM.setState(s);FILM.frame(c)},[s,cam]);await p.screenshot({path:path.join(OUT,'comparativo-'+k+'.png')});console.log('ok',k);}
 // 2) capas dos cards (1280x720), quadros-chave de cada vídeo
 const q=await page(1280,720);
 for(const [id,t] of (process.env.SO_COMP?[]:[['essencial',13.5],['acabamentos',25.2],['decorado',12.6],['cinematic',44.5]])){await q.evaluate(([i,t])=>RENDER(i,t),[id,t]);await q.screenshot({path:path.join(OUT,'capa-'+id+'.png')});console.log('capa',id);}
 await b.close();})();
