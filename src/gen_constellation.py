#!/usr/bin/env python3
"""데이터 → 인터랙티브 성좌(canvas) 플래그십 페이지. exhibits/constellation.html 생성."""
import json
ROOT="/home/djchoi/deokjinlog/classic-bones-modern-fusion"
SK=json.load(open(f"{ROOT}/data/skeletons.json",encoding="utf-8"))
ST=json.load(open(f"{ROOT}/data/settings.json",encoding="utf-8"))
PR=json.load(open(f"{ROOT}/data/premises.json",encoding="utf-8"))
bones=[{"k":k,"name":v.get("name",k),"req":v.get("req",[]),"proven":v.get("proven",0),
        "md":v.get("modern_done",0.5),"engine":v.get("engine","")}
       for k,v in SK.items() if not k.startswith("_")]
sets=[{"k":k,"name":v.get("name",k),"affords":v.get("affords",[]),"gloss":v.get("gloss","")}
      for k,v in ST.items() if not k.startswith("_")]
prem={k:v for k,v in PR.items() if not k.startswith("_")}
GL={"G1":"계층","G2":"금지된 사랑","G3":"승계·축취","G4":"귀향","G5":"감금","G6":"억압권력",
    "G7":"예언","G8":"부패권력","G9":"은폐진실","G10":"위장정체","G11":"마감","G12":"경제·부채",
    "G13":"강압·조종","G14":"평판","G15":"대리유대","G16":"여정","G17":"괴물","G18":"탐색물",
    "G19":"사부","G20":"신분상승","G21":"두 세계"}

T = r'''<title>매칭 성좌</title>
<style>
  :root{
    --void:#07060e; --ink:#eef0f7; --dim:#8b8aa0; --faint:#565471;
    --amber:#f7b23c; --amber2:#ffd27a; --cyan:#3fe0ff; --cyan2:#a5f0ff;
    --line:#221f33;
    --sans:"Apple SD Gothic Neo","Malgun Gothic","Noto Sans KR",system-ui,-apple-system,sans-serif;
  }
  *{box-sizing:border-box;margin:0;}
  html,body{height:100%;}
  body{background:var(--void);color:var(--ink);font-family:var(--sans);overflow:hidden;}
  #sky{position:fixed;inset:0;display:block;width:100%;height:100%;}
  .veil{position:fixed;inset:0;pointer-events:none;
    background:radial-gradient(60% 55% at 16% 12%, rgba(247,178,60,.14), transparent 60%),
               radial-gradient(60% 55% at 86% 90%, rgba(63,224,255,.13), transparent 60%),
               radial-gradient(120% 90% at 50% 120%, rgba(0,0,0,.55), transparent);}

  .hd{position:fixed;top:0;left:0;right:0;padding:26px 30px 0;pointer-events:none;}
  .eyebrow{font:800 11px var(--sans);letter-spacing:.34em;text-transform:uppercase;
    color:var(--amber);opacity:.9;}
  h1{margin:8px 0 0;font-weight:900;letter-spacing:-.035em;line-height:.98;
    font-size:clamp(30px,5.4vw,62px);text-wrap:balance;}
  h1 .a{background:linear-gradient(180deg,#fff,#f7b23c);-webkit-background-clip:text;background-clip:text;color:transparent;}
  h1 .x{color:var(--faint);font-weight:400;margin:0 .12em;}
  h1 .b{background:linear-gradient(180deg,#fff,#3fe0ff);-webkit-background-clip:text;background-clip:text;color:transparent;}
  .sub{margin-top:12px;max-width:44ch;color:var(--dim);font-size:14.5px;line-height:1.6;}
  .sub b{color:var(--ink);}
  .nav{margin-top:16px;display:flex;gap:18px;flex-wrap:wrap;pointer-events:auto;}
  .nav a{font:700 12.5px var(--sans);color:var(--dim);text-decoration:none;border-bottom:1px solid transparent;padding-bottom:2px;transition:.15s;}
  .nav a:hover{color:var(--ink);border-color:var(--amber);}

  .legend{position:fixed;top:26px;right:30px;display:flex;gap:16px;align-items:center;
    font:600 12px var(--sans);color:var(--dim);pointer-events:none;}
  .legend i{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:6px;vertical-align:middle;}
  .legend .ab{background:var(--amber);box-shadow:0 0 8px var(--amber);}
  .legend .cb{background:var(--cyan);box-shadow:0 0 8px var(--cyan);}
  .legend .ln{width:16px;height:2px;border-radius:2px;background:linear-gradient(90deg,var(--amber),var(--cyan));}

  .hud{position:fixed;left:30px;bottom:28px;width:min(380px,calc(100vw - 60px));
    border:1px solid var(--line);border-radius:18px;padding:18px 20px;
    background:linear-gradient(180deg, rgba(20,18,32,.82), rgba(12,11,20,.82));
    backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);
    box-shadow:0 30px 80px -40px #000; transition:opacity .3s;}
  .hud .setn{font-size:12px;letter-spacing:.06em;color:var(--cyan);font-weight:800;}
  .hud .arrow{color:var(--faint);margin:0 7px;}
  .hud .bn{font-size:23px;font-weight:900;letter-spacing:-.02em;margin-top:3px;line-height:1.1;}
  .hud .bn .amber{color:var(--amber);}
  .hud .eng{color:var(--dim);font-size:12.5px;margin-top:2px;}
  .hud .bars{display:grid;grid-template-columns:1fr 1fr 1fr;gap:11px;margin:15px 0 4px;}
  .hud .bk{font:800 9.5px var(--sans);letter-spacing:.1em;text-transform:uppercase;color:var(--faint);display:flex;justify-content:space-between;}
  .hud .bk b{color:var(--ink);font-size:12px;font-variant-numeric:tabular-nums;}
  .hud .tr{height:6px;border-radius:5px;background:#211f31;margin-top:5px;overflow:hidden;}
  .hud .fl{height:100%;border-radius:5px;}
  .fa{background:linear-gradient(90deg,#e29225,var(--amber));}
  .fc{background:linear-gradient(90deg,#1f9bb3,var(--cyan));}
  .fg{background:linear-gradient(90deg,#2f9e70,#54e0a0);}
  .hud .log{margin-top:14px;font-size:13.5px;line-height:1.62;color:var(--ink);border-top:1px solid var(--line);padding-top:13px;}
  .hud .comp{margin-top:9px;font-size:12px;color:var(--cyan);font-weight:700;}
  .hint{position:fixed;right:30px;bottom:30px;font:600 12px var(--sans);color:var(--faint);pointer-events:none;text-align:right;}
  .hint b{color:var(--amber);}
  .repo{position:fixed;left:30px;bottom:8px;font:600 10.5px var(--sans);color:#3a3850;text-decoration:none;pointer-events:auto;}
  @media(max-width:640px){ .legend,.hint{display:none;} .hd{padding:18px 20px 0;} .hud{left:14px;right:14px;bottom:14px;width:auto;} }
</style>

<canvas id="sky"></canvas>
<div class="veil"></div>

<div class="hd">
  <div class="eyebrow">classic-bones-modern-fusion</div>
  <h1><span class="a">고전 뼈대</span><span class="x">×</span><span class="b">현대 세팅</span></h1>
  <p class="sub">검증된 이야기 구조가 새 무대를 만나는 지도. <b>세팅(시안)에 다가가면</b> 맞는 <b>뼈대(앰버)</b>로 별이 이어진다 — 매칭은 코드가, 융합만 LLM이.</p>
  <nav class="nav">
    <a href="https://deokjinlog.github.io/classic-bones-modern-fusion/explore.html">🎯 매칭 탐색기</a>
    <a href="https://deokjinlog.github.io/classic-bones-modern-fusion/center.html">👑 웹툰 「센터」</a>
    <a href="https://deokjinlog.github.io/classic-bones-modern-fusion/cargo.html">🚀 웹툰 「화물」</a>
  </nav>
</div>
<div class="legend"><span><i class="ab"></i>뼈대 · 고전</span><span><i class="cb"></i>세팅 · 현대</span><span><i class="ln" style="border-radius:2px"></i>매칭</span></div>

<div class="hud" id="hud"></div>
<div class="hint"><b>호버</b>로 탐색 · <b>클릭</b>으로 고정</div>
<a class="repo" href="https://github.com/deokjinlog/classic-bones-modern-fusion">github.com/deokjinlog/classic-bones-modern-fusion</a>

<script>
const BONES=__BONES__, SETS=__SETS__, PREM=__PREM__, GL=__GL__;
const SBY={}; SETS.forEach(s=>SBY[s.k]=s);
const MAXPROV=Math.max(...BONES.map(b=>b.proven));
const cv=document.getElementById('sky'), ctx=cv.getContext('2d');
const reduce=matchMedia('(prefers-reduced-motion:reduce)').matches;
let W=0,H=0,DPR=1;
function resize(){ DPR=Math.min(2,window.devicePixelRatio||1); W=cv.clientWidth; H=cv.clientHeight;
  cv.width=W*DPR; cv.height=H*DPR; ctx.setTransform(DPR,0,0,DPR,0,0); }
addEventListener('resize',()=>{resize(); place();});

let nodes=[];
function place(){
  nodes=[];
  const pad=70, wt=W-pad*2, ht=H-pad*2;
  // bones: warm cluster upper-left biased; settings: cool lower-right biased
  BONES.forEach((b,i)=>{
    const gx=0.10+0.55*Math.random(), gy=0.08+0.6*Math.random();
    nodes.push(mk(b.k,'bone',b.name, pad+gx*wt, pad+gy*ht, 3+ (b.proven/MAXPROV)*6, b));
  });
  SETS.forEach((s,i)=>{
    const gx=0.35+0.6*Math.random(), gy=0.32+0.62*Math.random();
    nodes.push(mk(s.k,'set',s.name, pad+gx*wt, pad+gy*ht, 4.6, s));
  });
}
function mk(k,type,name,x,y,r,data){
  const ang=Math.random()*6.28, sp=reduce?0:0.05+Math.random()*0.12;
  return {k,type,name,x,y,r,data,vx:Math.cos(ang)*sp,vy:Math.sin(ang)*sp,
    z:0.35+Math.random()*0.65, ph:Math.random()*6.28, sx:x,sy:y};
}
const NBY={};
function reindex(){ nodes.forEach(n=>NBY[n.type+':'+n.k]=n); }

function matchesFor(setKey){
  const aff=SBY[setKey].affords;
  return BONES.map(b=>{
    const met=b.req.filter(c=>aff.includes(c)), rate=b.req.length?met.length/b.req.length:0;
    const fresh=1-b.md, score=rate>=0.999?fresh*b.proven:0;
    return {b,met,rate,fresh,score};
  }).filter(m=>m.score>0).sort((a,b)=>b.score-a.score);
}

let mouse={x:-999,y:-999,mx:0,my:0}, active=null, locked=true;
cv.addEventListener('pointermove',e=>{ const r=cv.getBoundingClientRect();
  mouse.x=e.clientX-r.left; mouse.y=e.clientY-r.top;
  mouse.mx=(mouse.x/W-0.5); mouse.my=(mouse.y/H-0.5);
  if(!locked) hoverPick(); else hoverPick(true); });
cv.addEventListener('pointerdown',e=>{ const r=cv.getBoundingClientRect();
  mouse.x=e.clientX-r.left; mouse.y=e.clientY-r.top; const n=nearestSet();
  if(n){ active=n.k; locked=true; renderHUD(); } });
cv.addEventListener('pointerleave',()=>{ mouse.x=-999; mouse.y=-999; });

function spos(n){ return {x:n.x+mouse.mx*40*n.z, y:n.y+mouse.my*40*n.z}; }
function nearestSet(){ let best=null,bd=44;
  nodes.forEach(n=>{ if(n.type!=='set')return; const p=spos(n); const d=Math.hypot(p.x-mouse.x,p.y-mouse.y);
    if(d<bd){bd=d;best=n;} }); return best; }
function hoverPick(soft){ const n=nearestSet();
  if(n){ if(active!==n.k){ active=n.k; locked=false; renderHUD(); } }
}

let cache={key:null,ms:[],top:null};
function ensure(){ if(cache.key!==active){ const ms=matchesFor(active); cache={key:active,ms,top:ms[0]||null}; } return cache; }

function renderHUD(){
  const s=SBY[active], c=ensure(), pk=PREM[active]; if(!s||!c.top){document.getElementById('hud').style.opacity=0;return;}
  const t=c.top;
  document.getElementById('hud').style.opacity=1;
  document.getElementById('hud').innerHTML=
    `<div><span class="setn">${s.name}</span><span class="arrow">→</span><span class="setn" style="color:var(--faint)">${c.ms.length} 적합</span></div>
     <div class="bn"><span class="amber">${t.b.name}</span></div><div class="eng">${t.b.engine}</div>
     <div class="bars">
       <div><div class="bk"><span>검증</span><b>${t.b.proven}</b></div><div class="tr"><div class="fl fa" style="width:${Math.round(t.b.proven/MAXPROV*100)}%"></div></div></div>
       <div><div class="bk"><span>신선</span><b>${Math.round(t.fresh*100)}%</b></div><div class="tr"><div class="fl fc" style="width:${Math.round(t.fresh*100)}%"></div></div></div>
       <div><div class="bk"><span>양립</span><b>${t.met.length}/${t.b.req.length}</b></div><div class="tr"><div class="fl fg" style="width:${Math.round(t.met.length/t.b.req.length*100)}%"></div></div></div>
     </div>
     ${pk?`<div class="log">${pk.l}</div><div class="comp">${pk.c}</div>`:''}`;
}

function hex(h,a){ const n=parseInt(h.slice(1),16); return `rgba(${n>>16&255},${n>>8&255},${n&255},${a})`; }
function frame(ts){
  const t=ts/1000;
  // physics
  const pad=60;
  nodes.forEach(n=>{ n.x+=n.vx; n.y+=n.vy;
    if(n.x<pad||n.x>W-pad) n.vx*=-1; if(n.y<pad||n.y>H-pad) n.vy*=-1;
    n.x=Math.max(pad,Math.min(W-pad,n.x)); n.y=Math.max(pad,Math.min(H-pad,n.y)); });
  ctx.clearRect(0,0,W,H);
  const c=active?ensure():null;
  const matchedSet=new Set(c?c.ms.map(m=>'bone:'+m.b.k):[]);
  const actNode=active?NBY['set:'+active]:null;
  // faint ambient links between nearby nodes (constellation feel)
  ctx.lineWidth=1;
  for(let i=0;i<nodes.length;i++){ const a=spos(nodes[i]);
    for(let j=i+1;j<nodes.length;j++){ const b=spos(nodes[j]); const d=Math.hypot(a.x-b.x,a.y-b.y);
      if(d<118){ ctx.strokeStyle=`rgba(150,150,190,${(1-d/118)*0.05})`; ctx.beginPath(); ctx.moveTo(a.x,a.y); ctx.lineTo(b.x,b.y); ctx.stroke(); } } }
  // active match lines
  if(actNode && c){ const ap=spos(actNode);
    c.ms.forEach((m,idx)=>{ const bn=NBY['bone:'+m.b.k]; if(!bn)return; const bp=spos(bn);
      const top=idx===0; const g=ctx.createLinearGradient(bp.x,bp.y,ap.x,ap.y);
      g.addColorStop(0,hex('#f7b23c',top?.95:.5)); g.addColorStop(1,hex('#3fe0ff',top?.95:.5));
      ctx.strokeStyle=g; ctx.lineWidth=top?2.4:1.1; ctx.beginPath(); ctx.moveTo(bp.x,bp.y); ctx.lineTo(ap.x,ap.y); ctx.stroke();
      if(top){ const tt=reduce?0.5:(t*0.35)%1; const px=bp.x+(ap.x-bp.x)*tt, py=bp.y+(ap.y-bp.y)*tt;
        ctx.fillStyle=hex('#ffffff',.9); ctx.beginPath(); ctx.arc(px,py,2.6,0,6.28); ctx.fill();
        ctx.fillStyle=hex('#ffe6a8',.4); ctx.beginPath(); ctx.arc(px,py,6,0,6.28); ctx.fill(); }
    });
  }
  // nodes
  nodes.forEach(n=>{ const p=spos(n); const isBone=n.type==='bone';
    const base=isBone?'#f7b23c':'#3fe0ff', glow=isBone?'#ffd27a':'#a5f0ff';
    let a=1, dim=false;
    if(active){ if(n.type==='set'){ a = n.k===active?1:0.16; }
      else { a = matchedSet.has('bone:'+n.k)?1:0.14; } }
    const isActS = n.type==='set'&&n.k===active;
    const isMatched = matchedSet.has('bone:'+n.k);
    const tw=0.75+0.25*Math.sin(t*1.4+n.ph);
    const rr=n.r*(isActS?1.5:1)*(reduce?1:(0.9+0.1*tw));
    // halo
    const hg=ctx.createRadialGradient(p.x,p.y,0,p.x,p.y,rr*5.5);
    hg.addColorStop(0,hex(glow, a*0.5*tw)); hg.addColorStop(1,hex(glow,0));
    ctx.fillStyle=hg; ctx.beginPath(); ctx.arc(p.x,p.y,rr*5.5,0,6.28); ctx.fill();
    // core
    ctx.fillStyle=hex(base,a); ctx.beginPath(); ctx.arc(p.x,p.y,rr,0,6.28); ctx.fill();
    ctx.fillStyle=hex('#ffffff',a*0.8); ctx.beginPath(); ctx.arc(p.x,p.y,rr*0.4,0,6.28); ctx.fill();
    // labels: only active set + matched bones (+ active bone ring)
    const showLabel = (isActS) || (active&&isMatched) ;
    if(showLabel){ ctx.font=`${isActS?'700 13px':'600 11.5px'} var(--sans)`;
      ctx.fillStyle=hex(isBone?glow:'#d8f6ff', 0.96); ctx.textAlign='center';
      ctx.fillText(n.name, p.x, p.y - rr - 7); }
    if(isActS){ ctx.strokeStyle=hex(base,.7); ctx.lineWidth=1.4; ctx.beginPath(); ctx.arc(p.x,p.y,rr+6,0,6.28); ctx.stroke(); }
  });
  requestAnimationFrame(frame);
}

resize(); place(); reindex();
active = SBY['아이돌기획사']?'아이돌기획사':SETS[0].k; locked=true; renderHUD();
requestAnimationFrame(frame);
</script>'''

out=(T.replace("__BONES__",json.dumps(bones,ensure_ascii=False))
      .replace("__SETS__",json.dumps(sets,ensure_ascii=False))
      .replace("__PREM__",json.dumps(prem,ensure_ascii=False))
      .replace("__GL__",json.dumps(GL,ensure_ascii=False)))
open(f"{ROOT}/exhibits/constellation.html","w",encoding="utf-8").write(out)
print("constellation.html",len(out),"bytes ·",len(bones),"bones ·",len(sets),"settings")
