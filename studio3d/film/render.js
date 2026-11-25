// uso: node render.js <video> <h|v> <worker> <workers> [t1,t2,... (teste)]
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
const [id,orient,wk,nw,tests]=process.argv.slice(2);
const W=orient==='v'?1080:1920,H=orient==='v'?1920:1080,FPS=24;
(async()=>{
 const b=await chromium.launch({args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--allow-file-access-from-files']});
 const p=await b.newPage({viewport:{width:W,height:H}});
 const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
 await p.goto('file://'+__dirname+'/film.html');
 await p.waitForFunction('window.FILM && window.RENDER',{timeout:60000});
 await p.evaluate(()=>window.FILM.ready);await p.evaluate(()=>document.fonts.ready);
 const dur=await p.evaluate(i=>VIDEOS[i].dur,id);
 const out=path.join(__dirname,'frames',id+'_'+orient);fs.mkdirSync(out,{recursive:true});
 if(tests){ for(const t of tests.split(',').map(Number)){const t0=Date.now();await p.evaluate(([i,t])=>RENDER(i,t),[id,t]);await p.screenshot({path:path.join(__dirname,'frames','test_'+id+'_'+orient+'_'+t+'.jpg'),type:'jpeg',quality:90});console.log('t',t,Date.now()-t0,'ms');} console.log('erros',errs.slice(0,5));await b.close();return;}
 const N=Math.round(dur*FPS);let n=0;const t0=Date.now();
 for(let i=+wk;i<N;i+=+nw){const f=path.join(out,String(i).padStart(5,'0')+'.jpg');if(fs.existsSync(f)){continue;}
   await p.evaluate(([v,t])=>RENDER(v,t),[id,i/FPS]);await p.screenshot({path:f+'.tmp.jpg',type:'jpeg',quality:93});fs.renameSync(f+'.tmp.jpg',f);n++;
   if(n%40===0)console.log(id,orient,'w'+wk,i,'/',N,((Date.now()-t0)/n/1000).toFixed(2)+'s/q');}
 console.log('fim',id,orient,'w'+wk,'erros',errs.slice(0,5));await b.close();})();
