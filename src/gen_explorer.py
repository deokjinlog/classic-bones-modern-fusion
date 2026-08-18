#!/usr/bin/env python3
import json, re
ROOT="/home/djchoi/deokjinlog/classic-bones-modern-fusion"
SK=json.load(open(f"{ROOT}/data/skeletons.json",encoding="utf-8"))
ST=json.load(open(f"{ROOT}/data/settings.json",encoding="utf-8"))
sk={k:{"name":v.get("name",k),"engine":v.get("engine",""),"req":v.get("req",[]),
       "proven":v.get("proven",0),"md":v.get("modern_done",0.5),"freq":v.get("freq",0),"cf":v.get("canon_freq",0),
       "roles":v.get("roles",[]),"turns":v.get("turns",[])}
    for k,v in SK.items() if not k.startswith("_")}
# 검증도(proven) 내림차순 순위 (동점은 공동)
_pr_sorted=sorted({s["proven"] for s in sk.values()}, reverse=True)
_provrank={p:i+1 for i,p in enumerate(_pr_sorted)}
for s in sk.values(): s["prank"]=_provrank[s["proven"]]
st={k:{"name":v.get("name",k),"affords":v.get("affords",[]),"gloss":v.get("gloss","")}
    for k,v in ST.items() if not k.startswith("_")}
PR=json.load(open(f"{ROOT}/data/premises.json",encoding="utf-8"))
pr={k:v for k,v in PR.items() if not k.startswith("_")}
try:
    CN=json.load(open(f"{ROOT}/data/census.json",encoding="utf-8")); cs=CN.get("settings",{}); cmeta=CN.get("_meta",{})
except FileNotFoundError:
    cs={}; cmeta={"total":0,"n_settings":0}
GL={"G1":"계층 격차","G2":"금지된 사랑","G3":"승계·축취","G4":"귀환할 집","G5":"감금",
    "G6":"억압 권력","G7":"예언·운명","G8":"부패 권력","G9":"은폐된 진실","G10":"위장·이중정체",
    "G11":"마감","G12":"경제·부채","G13":"강압·조종","G14":"평판·명예","G15":"대리·유대",
    "G16":"여정·원정","G17":"괴물·위협","G18":"탐색물","G19":"사부·수련","G20":"신분 상승","G21":"두 세계"}

T = r'''<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>고전 뼈대 매칭 탐색기</title>
<style>
  :root{
    --stage:#0e0d14; --panel:#16141d; --panel2:#1c1a26; --ink:#f3eff7; --muted:#9a94a6; --faint:#67626f;
    --gold:#f6c453; --magenta:#ff2e88; --cyan:#35e6ff; --good:#54e0a0; --bad:#e5556f;
    --line:#242231; --line2:#332f3f;
    --sans:"Apple SD Gothic Neo","Malgun Gothic","Noto Sans KR",system-ui,-apple-system,sans-serif;
  }
  *{box-sizing:border-box;} html{-webkit-text-size-adjust:100%;}
  body{margin:0;background:var(--stage);color:var(--ink);font-family:var(--sans);line-height:1.6;-webkit-font-smoothing:antialiased;overflow-x:hidden;}
  .wrap{max-width:880px;margin:0 auto;padding:30px 18px 70px;}
  .kicker{font-size:11px;letter-spacing:.28em;text-transform:uppercase;color:var(--gold);font-weight:800;margin:0 0 8px;overflow-wrap:anywhere;}
  h1{font-size:clamp(26px,6vw,40px);font-weight:900;letter-spacing:-.03em;margin:0;line-height:1.05;text-wrap:balance;}
  .lead{margin:12px 0 0;color:var(--muted);font-size:14.5px;max-width:62ch;}
  .lead b{color:var(--ink);}

  .picklbl{font-size:11px;letter-spacing:.22em;text-transform:uppercase;color:var(--faint);font-weight:800;margin:26px 0 12px;display:flex;gap:12px;align-items:center;}
  .picklbl::after{content:"";flex:1;height:1px;background:linear-gradient(90deg,var(--line2),transparent);}
  .picker{display:flex;flex-wrap:wrap;gap:7px;}
  .chip{border:1px solid var(--line2);background:var(--panel);color:var(--muted);border-radius:999px;
    padding:7px 13px;font:600 13px var(--sans);cursor:pointer;transition:.14s;}
  .chip:hover{border-color:var(--gold);color:var(--ink);}
  .chip[aria-pressed="true"]{background:var(--gold);color:#241a06;border-color:var(--gold);font-weight:800;}
  .chip.feat{border-color:var(--gold);box-shadow:0 0 0 1px var(--gold) inset;color:var(--ink);}
  .chip.feat[aria-pressed="true"]{box-shadow:none;}
  .feathint{font-size:.82em;color:var(--gold);font-weight:700;letter-spacing:0;}
  .byos{margin:24px 0 6px;padding:16px 18px;border:1px solid var(--line2);border-radius:14px;background:linear-gradient(180deg,rgba(246,196,83,.055),transparent);}
  .byos-h{font-size:14px;color:var(--ink);margin-bottom:12px;line-height:1.55;}
  .byos-h>b{color:var(--gold);}
  .byos-sub{color:var(--faint);font-size:12.5px;font-weight:400;}
  .byos-sub b{color:var(--muted);font-weight:700;}
  .byos-in{display:flex;gap:8px;}
  #byoq{flex:1;min-width:0;background:var(--panel);border:1px solid var(--line2);border-radius:9px;padding:10px 13px;color:var(--ink);font:500 14px var(--sans);}
  #byoq:focus{outline:none;border-color:var(--gold);}
  #byob{background:var(--gold);color:#241a06;border:none;border-radius:9px;padding:0 16px;font:800 13px var(--sans);cursor:pointer;white-space:nowrap;}
  .byotags{margin-top:13px;display:flex;flex-wrap:wrap;gap:6px;align-items:center;}
  .byhint{color:var(--faint);font-size:11.5px;margin-bottom:2px;width:100%;}
  .btag{border:1px solid var(--line2);background:var(--panel);color:var(--muted);border-radius:999px;padding:5px 10px;font:600 11.5px var(--sans);cursor:pointer;transition:.12s;}
  .btag:hover{border-color:var(--gold);}
  .btag.on{background:var(--gold);color:#241a06;border-color:var(--gold);font-weight:800;}
  .pk-note{margin:0;font-size:13.5px;color:var(--muted);line-height:1.75;}
  .pk-note b{color:var(--ink);}
  .sharebar{display:flex;justify-content:flex-end;margin-bottom:6px;}
  .copyl{background:var(--panel);border:1px solid var(--line2);color:var(--muted);border-radius:8px;padding:5px 11px;font:700 11.5px var(--sans);cursor:pointer;white-space:nowrap;transition:.12s;}
  .copyl:hover{border-color:var(--gold);color:var(--ink);}
  .rnd{border:1px dashed var(--line2);background:transparent;color:var(--gold);border-radius:999px;padding:7px 13px;font:700 13px var(--sans);cursor:pointer;}
  .rnd:hover{border-color:var(--gold);}

  .setline{margin:26px 0 4px;display:flex;flex-wrap:wrap;align-items:baseline;gap:10px;}
  .setname{font-size:20px;font-weight:900;}
  .setgloss{color:var(--faint);font-size:12.5px;overflow-wrap:anywhere;min-width:0;}
  .affords{margin:10px 0 0;display:flex;flex-wrap:wrap;gap:6px;align-items:center;font-size:12px;color:var(--faint);}
  .gtag{border:1px solid var(--line2);border-radius:6px;padding:3px 8px;font:600 11.5px var(--sans);color:var(--muted);background:var(--panel);}

  .top{margin:16px 0 0;border:1px solid var(--line2);border-radius:16px;overflow:hidden;background:linear-gradient(180deg,var(--panel2),var(--panel));}
  .top .hd{padding:16px 18px 14px;border-bottom:1px solid var(--line);}
  .toptag{display:inline-block;font:800 10.5px var(--sans);letter-spacing:.16em;text-transform:uppercase;color:#241a06;background:var(--gold);border-radius:999px;padding:4px 10px;margin-bottom:10px;}
  .top h2{margin:0;font-size:22px;font-weight:900;}
  .top .engine{color:var(--muted);font-weight:600;font-size:14px;}
  .bars{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;padding:16px 18px;}
  @media(max-width:560px){.bars{grid-template-columns:1fr;}}
  .bar .bk{font:800 10.5px var(--sans);letter-spacing:.12em;text-transform:uppercase;color:var(--faint);display:flex;justify-content:space-between;}
  .bar .bk b{color:var(--ink);font-size:13px;font-variant-numeric:tabular-nums;}
  .bar .track{height:8px;border-radius:6px;background:#26232f;margin-top:6px;overflow:hidden;}
  .bar .fill{height:100%;border-radius:6px;}
  .f-gold{background:linear-gradient(90deg,#e6a53a,var(--gold));}
  .f-cyan{background:linear-gradient(90deg,#1f9bb3,var(--cyan));}
  .f-good{background:linear-gradient(90deg,#2f9e70,var(--good));}
  .reqline{padding:0 18px 16px;display:flex;flex-wrap:wrap;gap:6px;align-items:center;font-size:12px;color:var(--faint);}
  .met{border:1px solid #2a5f49;background:#0e2019;color:var(--good);border-radius:6px;padding:3px 8px;font:700 11.5px var(--sans);}
  .flow{padding:14px 18px;border-top:1px solid var(--line);font-size:13px;color:var(--muted);}
  .flow b{color:var(--ink);} .flow .arrow{color:var(--gold);}
  code{font-family:ui-monospace,"SF Mono",Menlo,Consolas,monospace;font-size:12px;color:var(--cyan);background:rgba(53,230,255,.07);padding:1px 6px;border-radius:5px;}
  .metrics{padding:14px 18px 4px;border-top:1px solid var(--line);display:flex;flex-direction:column;gap:9px;font-size:12.5px;color:var(--muted);line-height:1.5;}
  .metrics>div{overflow-wrap:anywhere;}
  .metrics .mk{display:inline-block;min-width:44px;font:800 10px var(--sans);letter-spacing:.12em;text-transform:uppercase;color:var(--faint);}
  .metrics b{color:var(--ink);font-variant-numeric:tabular-nums;} .metrics .dim{color:var(--faint);}
  .metrics .met,.metrics .missc{margin-right:4px;}
  .rmid{min-width:0;} .rbar{height:4px;border-radius:3px;background:#26232f;margin-top:7px;overflow:hidden;max-width:280px;}
  .rfill{height:100%;background:linear-gradient(90deg,#8a6a2a,var(--gold));border-radius:3px;}
  .row .sc .lab{white-space:nowrap;}
  .packet{margin-top:12px;border:1px solid var(--line2);border-radius:16px;overflow:hidden;background:linear-gradient(180deg,#191622,var(--panel));}
  .pk-h{padding:12px 18px;border-bottom:1px solid var(--line);font:800 11px var(--sans);letter-spacing:.18em;text-transform:uppercase;color:var(--gold);display:flex;align-items:center;gap:10px;}
  .pk-tag{font-size:9.5px;letter-spacing:.08em;color:var(--muted);border:1px solid var(--line2);border-radius:999px;padding:2px 8px;text-transform:none;}
  .pk-row{display:grid;grid-template-columns:66px 1fr;gap:14px;padding:12px 18px;border-top:1px solid var(--line);}
  .pk-k{font:800 10.5px var(--sans);letter-spacing:.1em;text-transform:uppercase;color:var(--faint);padding-top:3px;}
  .pk-row p{margin:0;min-width:0;font-size:14px;color:var(--ink);line-height:1.72;overflow-wrap:anywhere;}
  .pk-comp{color:var(--cyan)!important;font-weight:700;}
  .pk-deep{border-top:1px solid var(--line2);margin-top:2px;padding:14px 18px 6px;display:flex;flex-direction:column;gap:12px;background:linear-gradient(180deg,rgba(255,46,136,.045),transparent);}
  .pk-deep>div{display:grid;grid-template-columns:48px 1fr;gap:12px;}
  .pk-deep .dk{font:800 10px var(--sans);letter-spacing:.08em;text-transform:uppercase;color:var(--magenta);padding-top:3px;}
  .pk-deep p{margin:0;font-size:13.5px;line-height:1.66;color:var(--ink);}
  .pk-map{display:grid;gap:5px;font-size:13px;line-height:1.4;}
  .pk-map>div{display:flex;align-items:baseline;gap:2px;flex-wrap:wrap;}
  .pk-map .rl{color:var(--faint);min-width:92px;} .pk-map .ar{color:var(--gold);margin:0 7px;} .pk-map b{color:var(--ink);}
  .pk-arc{margin:2px 0 0;padding-left:20px;font-size:13.5px;color:var(--ink);line-height:1.68;}
  .pk-arc li{margin:3px 0;} .pk-arc li::marker{color:var(--gold);font-weight:800;}

  .ranklbl{font-size:11px;letter-spacing:.22em;text-transform:uppercase;color:var(--faint);font-weight:800;margin:30px 0 10px;}
  .rows{display:flex;flex-direction:column;gap:6px;}
  .row{display:grid;grid-template-columns:26px 1fr auto;gap:12px;align-items:center;border:1px solid var(--line);border-radius:11px;padding:11px 14px;background:var(--panel);}
  .row>span{min-width:0;overflow-wrap:anywhere;}
  .row.miss{opacity:.5;}
  .row .num{font:900 14px var(--sans);color:var(--faint);font-variant-numeric:tabular-nums;text-align:right;}
  .row .rn{font-weight:800;font-size:14.5px;}
  .row .re{color:var(--faint);font-size:11.5px;}
  .row .sc{text-align:right;font-variant-numeric:tabular-nums;}
  .row .sc b{color:var(--gold);font-size:15px;font-weight:900;}
  .row .sc .lab{color:var(--faint);font-size:10px;letter-spacing:.1em;text-transform:uppercase;display:block;}
  .row.miss .sc b{color:var(--bad);font-size:12px;}
  .row .missc{color:var(--bad);}
  .row.aug{border-color:#4a3a1e;background:linear-gradient(90deg,rgba(246,196,83,.08),var(--panel));align-items:start;}
  .augtip{margin-top:5px;font-size:12px;color:var(--muted);line-height:1.5;} .augtip b{color:var(--gold);}
  .row.aug .num{color:var(--gold);font-size:15px;}
  .augb{color:var(--gold)!important;font-size:12px!important;}

  .note{margin-top:26px;border:1px solid var(--line2);border-radius:14px;padding:16px 18px;background:var(--panel);font-size:13.5px;color:var(--muted);}
  .note b{color:var(--ink);} .note .k{color:var(--gold);font-weight:800;}
  .foot{margin-top:22px;text-align:center;font-size:12px;color:var(--faint);}
  .foot a{color:var(--magenta);text-decoration:none;}
</style>

<div class="wrap">
  <p class="kicker">classic-bones-modern-fusion · 매칭 엔진</p>
  <h1>고전 뼈대 매칭 탐색기</h1>
  <p class="lead">현대 <b>세팅</b>을 하나 고르면 — 수백 년 검증된 <b>고전 뼈대</b> 중 무엇이 맞는지, <b>왜</b>인지를
    코드가 <b>결정적으로</b> 계산한다. <b>매칭은 취향 0</b>(요구 ⊆ 보유), 점수 = 신선도 × 검증도. 프리미스(융합)만 LLM이 쓴다.</p>

  <p class="picklbl">세팅 고르기 · __NSET__ &nbsp;<span class="feathint">⭐ 깊이 완성 사례 — 먼저 눌러보세요</span></p>
  <div class="picker" id="picker"></div>

  <div class="byos">
    <div class="byos-h">🧪 <b>내 세팅으로 해보기</b> <span class="byos-sub">— 아무 현대 세팅이나 넣으면 맞는 고전 뼈대를 <b>코드가 결정적으로</b> 찾아줍니다. 프리미스 프로즈만 skill 몫.</span></div>
    <div class="byos-in">
      <input id="byoq" placeholder="예: 대형 물류센터 · 국회 인턴실 · 대학병원 응급실 · 심해 시추선" autocomplete="off" spellcheck="false">
      <button id="byob">매칭 →</button>
    </div>
    <div id="byotags" class="byotags" hidden></div>
  </div>

  <div id="result"></div>

  <div class="note">
    <code>score = (1 − 소진) × proven</code> &nbsp;·&nbsp; 양립(요구 ⊆ 보유) 통과만 후보 &nbsp;·&nbsp; <code>proven = 일반 빈도 + 캐논 × 8</code>
    &nbsp;·&nbsp; 매칭·순위는 코드가 결정, 프리미스 문장만 LLM.
  </div>
  <p class="foot">classic-bones-modern-fusion · <a href="https://github.com/deokjinlog/classic-bones-modern-fusion">github.com/deokjinlog/classic-bones-modern-fusion</a></p>
</div>

<script>
const SK=__SK__, ST=__ST__, GL=__GL__, PR=__PR__, CS=__CS__, CTOT=__CTOT__, CNS=__CNS__, FEAT=__FEAT__, DOM=__DOM__;
const GADD={G1:"명확한 서열·계급 라인 만들기",G2:"규칙·장벽으로 갈린 관계 넣기",G3:"뺏고 뺏길 자리·상속 라인 만들기",G4:"떠났다 돌아올 원점(본진·고향) 두기",G5:"물리·사회적으로 갇힌 상태 넣기",G6:"감시·통제하는 상위 권력 두기",G7:"구속력 있는 예언·정해진 운명 넣기",G8:"쥐면 타락하는 자리·이권 두기",G9:"밝혀질 숨겨진 사실 하나 심기",G10:"정체를 숨기거나 쪼갤 여지(가면·이중신분) 넣기",G11:"절정을 강제하는 시한·데드라인 넣기",G12:"돈·빚·생계 압박 걸기",G13:"의지를 꺾는 계략·회유 넣기",G14:"공적 평판이 무기가 되는 판 만들기",G15:"비혈연 든든한 유대(팀·의형제) 넣기",G16:"목적지로 이동하는 원정·출장 구조 넣기",G17:"세계에 풀린 비인간 치명 위협 넣기",G18:"얻을·지킬·부술 특정 대상(맥거핀) 두기",G19:"사사받을 스승·전통 넣기",G20:"오를 사다리·일생일대 기회 넣기",G21:"맞닿는 두 영역(현실/가상 등) 넣기"};
const TAG={
 G1:["서열","계급","위계","랭킹","등급","기수","짬","순위","계층"],
 G2:["금지","장벽","벽","규칙","금기","계급차","신분차","라이벌","연애금지","넘지"],
 G3:["승계","후계","상속","왕좌","대표","후임","의장","회장","자리다툼","지분","센터 자리"],
 G4:["고향","귀향","귀농","본진","돌아","향수","고국","원점","금의환향"],
 G5:["감금","갇힌","수용","교도","감옥","격리","폐쇄","억류","구금","병실","섬","고립"],
 G6:["감시","통제","관제","상부","본사","경영진","위원회","관리","당국","시스템","알고리즘","플랫폼","본부"],
 G7:["예언","운명","숙명","정해진","점지","계시"],
 G8:["권력","이권","부패","정치","뇌물","비리","스캠","사기","횡령","커넥션","카르텔","로비","국회","청와대"],
 G9:["은폐","비밀","조작","감춘","숨긴","진실","폭로","내부고발","기밀","은닉","묻은","덮은","수사","형사","프로파일러","탐정","경찰","사건"],
 G10:["위장","잠입","가면","익명","이중","정체","신분세탁","언더커버","사칭","도용","부계정","클론","위조"],
 G11:["마감","데드라인","시한","카운트다운","생방송","실시간","컴백","론칭","출시","오픈","경기당일","선거일"],
 G12:["돈","빚","부채","파산","생계","대출","자금","투자","월세","코인","연봉","보증금","적자","펀딩"],
 G13:["조종","회유","세뇌","협박","압박","가스라이팅","계략","선동","여론몰이","길들","포섭"],
 G14:["평판","명예","여론","이미지","팔로워","조회수","인기","스타","화제","랭커","명성","리뷰","별점","셀럽"],
 G15:["팀","동료","크루","의형제","유사가족","하우스메이트","파티","길드","동아리","조합","멤버","동기","길드","레이드"],
 G16:["여정","원정","출장","항해","배달","이동","로드","탐사","순회","파견","원격지","시추","탐험","라이더","택배"],
 G17:["괴물","재난","바이러스","팬데믹","위협","몬스터","붕괴","폭주","화재","지진","해킹","돌연변이","ai","인공지능","좀비"],
 G18:["화물","유물","특종","단서","데이터","모델","아이템","증거","보물","레시피","소스코드","백신","맥거핀","비급"],
 G19:["사부","스승","지도교수","코치","트레이너","멘토","수련","도제","선임","마스터","선배","교관"],
 G20:["상승","데뷔","오디션","사다리","기회","발탁","승급","우승","대회","등단","스카웃","입봉","승진","콘테스트","인턴"],
 G21:["가상","현실","메타버스","vr","게임","이세계","두 세계","온오프","시뮬","증강","아바타","디지털"]};
let byoAff=[];
function autotag(t){t=(t||'').toLowerCase();const on=new Set();
  for(const kw in DOM){ if(t.includes(kw) && ST[DOM[kw]]) ST[DOM[kw]].affords.forEach(g=>on.add(g)); }
  for(const g in TAG){ if(TAG[g].some(w=>t.includes(w))) on.add(g); }
  return [...on];}
function paintTags(){
  const box=document.getElementById('byotags'); box.hidden=false;
  box.innerHTML='<span class="byhint">조건(입력에서 자동 제안 · 클릭해 켜고 끄면 매칭이 실시간으로 바뀝니다):</span>'+
    Object.keys(GADD).map(g=>`<button class="btag${byoAff.includes(g)?' on':''}" data-g="${g}">${g} ${gname(g)}</button>`).join('');
  box.querySelectorAll('.btag').forEach(b=>b.onclick=()=>{const g=b.dataset.g; byoAff=byoAff.includes(g)?byoAff.filter(x=>x!==g):[...byoAff,g]; paintTags(); runByo(); byoURL();});
}
function runByo(){const q=(document.getElementById('byoq').value||'').trim()||'내 세팅'; paint({name:q, gloss:'직접 입력한 세팅 · 태그로 조건 지정', aff:byoAff, cs:null, pk:null, key:null});}
function submitByo(){const q=(document.getElementById('byoq').value||'').trim(); if(!q)return; byoAff=autotag(q); paintTags(); runByo(); byoURL();}
function updateURL(qs){ try{history.replaceState(null,'',location.pathname+'?'+qs);}catch(e){} }
function pick(k){ render(k); updateURL('s='+encodeURIComponent(k)); }
function byoURL(){ updateURL('q='+encodeURIComponent((document.getElementById('byoq').value||'').trim())+'&g='+byoAff.join('.')); }
function copyLink(b){ try{navigator.clipboard.writeText(location.href).then(()=>{const t=b.textContent;b.textContent='✓ 복사됨';setTimeout(()=>b.textContent=t,1300);},()=>{}); }catch(e){} }
const MAXPROV=Math.max(...Object.values(SK).map(s=>s.proven)), NSK=Object.keys(SK).length;
const gname=c=>GL[c]||c;
function rows(aff){
  return Object.keys(SK).map(k=>{
    const s=SK[k], met=s.req.filter(c=>aff.includes(c)), miss=s.req.filter(c=>!aff.includes(c));
    const rate=s.req.length?met.length/s.req.length:0, fresh=1-s.md;
    const score=rate>=0.999?fresh*s.proven:0;
    return {k,name:s.name,engine:s.engine,req:s.req,met,miss,rate,fresh,proven:s.proven,prank:s.prank,freq:s.freq,cf:s.cf,score,roles:s.roles,turns:s.turns};
  }).sort((a,b)=> b.score-a.score || b.rate-a.rate);
}
function bar(lab,val,disp,cls){return `<div class="bar"><div class="bk"><span>${lab}</span><b>${disp}</b></div><div class="track"><div class="fill ${cls}" style="width:${Math.round(val*100)}%"></div></div></div>`;}
function render(setKey){ paint({name:ST[setKey].name, gloss:ST[setKey].gloss, aff:ST[setKey].affords, cs:CS[setKey], pk:PR[setKey], key:setKey}); }
function paint(cfg){
  const aff=cfg.aff, rs=rows(aff), top=rs[0], maxSc=Math.max(...rs.map(r=>r.score))||1;
  const affh=aff.map(c=>`<span class="gtag">${c} ${gname(c)}</span>`).join("");
  let h=`<div class="sharebar"><button class="copyl" onclick="copyLink(this)">🔗 이 매칭 링크 복사</button></div>
    <div class="setline"><span class="setname">${cfg.name}</span><span class="setgloss">${cfg.gloss||''}</span></div>
    <div class="affords">보유 조건 ${aff.length} · ${affh||'<span class="dim">아직 조건이 없어요 — 아래 태그를 켜보세요</span>'}</div>`;
  if(top && top.score>0){
    const metchips=top.req.map(c=> top.met.includes(c)?`<span class="met">✓ ${c} ${gname(c)}</span>`:`<span class="gtag missc">✗ ${c} ${gname(c)}</span>`).join("");
    h+=`<div class="top"><div class="hd"><span class="toptag">1등 매칭</span>
      <h2>${top.name} <span class="engine">— ${top.engine}</span></h2></div>
      <div class="bars">
        ${bar("검증 proven", top.proven/MAXPROV, top.proven, "f-gold")}
        ${bar("신선 freshness", top.fresh, Math.round(top.fresh*100)+"%", "f-cyan")}
        ${bar("양립 fit", top.met.length/top.req.length, top.met.length+"/"+top.req.length, "f-good")}
      </div>
      <div class="metrics">
        <div><span class="mk">검증</span> <code>proven ${top.proven} = 빈도 ${top.freq} + 캐논 ${top.cf}×8</code> · 전체 <b>${top.prank}/${NSK}위</b></div>
        <div><span class="mk">양립</span> ${metchips}</div>
        <div><span class="mk">신선</span> <code>1 − 소진 ${(1-top.fresh).toFixed(2)}</code> = <b>${Math.round(top.fresh*100)}%</b> <span class="dim">(순위용 추정)</span></div>
        ${cfg.cs?`<div><span class="mk">실측</span> 이 도메인은 실제 이야기 <code>${cfg.cs.pct}%</code>에 등장 <span class="dim">(WikiPlots ${cfg.cs.n.toLocaleString()}/${CTOT.toLocaleString()}편 · 희소도 ${cfg.cs.rarity_rank}/${CNS}위)</span></div>`:''}
      </div>
      <div class="flow"><b>역할</b> ${top.roles.join(" · ")}<br><b>턴</b> ${top.turns.join(' <span class="arrow">→</span> ')}</div>
    </div>`;
  }
  const pk=cfg.pk;
  if(pk){ h+=`<div class="packet"><div class="pk-h">피칭 패킷 <span class="pk-tag">융합 · LLM 생성</span></div>
    <div class="pk-row"><span class="pk-k">프리미스</span><p>${pk.p}</p></div>
    <div class="pk-row"><span class="pk-k">로그라인</span><p>${pk.l}</p></div>
    ${(top&&pk.rm)?`<div class="pk-row"><span class="pk-k">인물</span><div class="pk-map">${top.roles.map((r,i)=>`<div><span class="rl">${r}</span><span class="ar">→</span><b>${pk.rm[i]||'—'}</b></div>`).join("")}</div></div>`:''}
    ${pk.a?`<div class="pk-row"><span class="pk-k">전개</span><ol class="pk-arc">${pk.a.map(b=>`<li>${b}</li>`).join("")}</ol></div>`:''}
    <div class="pk-row"><span class="pk-k">comp</span><p class="pk-comp">${pk.c}</p></div>
    ${(pk.hk||pk.tw||pk.th||pk.wn)?`<div class="pk-deep">
      ${pk.hk?`<div><span class="dk">훅</span><p>${pk.hk}</p></div>`:''}
      ${pk.tw?`<div><span class="dk">반전</span><p>${pk.tw}</p></div>`:''}
      ${pk.th?`<div><span class="dk">주제</span><p>${pk.th}</p></div>`:''}
      ${pk.wn?`<div><span class="dk">욕망</span><p>${pk.wn}</p></div>`:''}
    </div>`:''}
    </div>`; }
  else if(cfg.key===null && top && top.score>0){ h+=`<div class="packet"><div class="pk-h">피칭 패킷 <span class="pk-tag">skill로 생성</span></div>
    <p class="pk-note">여기까지 — <b>구조 매칭·근거는 코드가 결정적으로</b> 끝냈습니다. 이 세팅의 깊은 프리미스·전개·반전 프로즈는 스킬 <code>classic-bones-fusion</code>이 씁니다. <b>매칭이 조준을 끝내면, 문장만 LLM이 씁니다.</b></p></div>`; }
  const matched=rs.filter(r=>r.score>0), missed=rs.filter(r=>r.score===0);
  const near=missed.filter(r=>r.miss.length===1), far=missed.filter(r=>r.miss.length>1);
  h+=`<p class="ranklbl">적합 ${matched.length} · 보강하면 가능 ${near.length} · 탈락 ${far.length}</p><div class="rows">`;
  matched.forEach((r,i)=>{ const gap=matched[0].score-r.score, lab=i===0?"점수":`Δ${gap.toFixed(1)} ${gap<2?"근소":gap<8?"우위":"압도"}`;
    h+=`<div class="row"><span class="num">${i+1}</span>
    <span class="rmid"><span class="rn">${r.name}</span> <span class="re">· ${r.engine}</span>
      <div class="rbar"><div class="rfill" style="width:${Math.round(r.score/maxSc*100)}%"></div></div></span>
    <span class="sc"><b>${r.score.toFixed(1)}</b><span class="lab">${lab}</span></span></div>`; });
  near.forEach(r=>{ const c=r.miss[0];
    h+=`<div class="row aug"><span class="num">🔧</span>
      <span><span class="rn">${r.name}</span> <span class="re">· ${r.engine}</span>
        <div class="augtip">한 끗 부족: <b>${c} ${gname(c)}</b> — ${GADD[c]||"이 조건을 세팅에 더하기"}</div></span>
      <span class="sc"><b class="augb">보강 시</b><span class="lab">가능</span></span></div>`; });
  far.slice(0,5).forEach(r=>{ h+=`<div class="row miss"><span class="num">—</span>
    <span><span class="rn">${r.name}</span> <span class="re">· ${r.engine}</span></span>
    <span class="sc"><b>탈락</b><span class="lab missc">${r.miss.map(gname).slice(0,2).join(" · ")} 없음</span></span></div>`; });
  h+=`</div>`;
  document.getElementById("result").innerHTML=h;
  [...document.querySelectorAll(".chip")].forEach(c=>c.setAttribute("aria-pressed", c.dataset.k===cfg.key));
}
(function(){
  const p=document.getElementById("picker");
  Object.keys(ST).forEach(k=>{ const b=document.createElement("button"); const feat=FEAT.includes(k);
    b.className="chip"+(feat?" feat":""); b.dataset.k=k; b.textContent=(feat?"⭐ ":"")+ST[k].name; b.setAttribute("aria-pressed","false");
    b.onclick=()=>pick(k); p.appendChild(b); });
  const r=document.createElement("button"); r.className="rnd"; r.textContent="🎲 자동 제안";
  r.onclick=()=>{ const ks=Object.keys(ST); pick(ks[Math.floor(Math.random()*ks.length)]); }; p.appendChild(r);
  document.getElementById("byob").onclick=submitByo;
  document.getElementById("byoq").addEventListener("keydown",e=>{if(e.key==="Enter")submitByo();});
  // 딥링킹: ?s=<세팅> 프리셋 · ?q=<입력>(&g=G1.G8 조건) BYOS
  const P=new URLSearchParams(location.search);
  if(P.get('s') && ST[P.get('s')]) render(P.get('s'));
  else if(P.get('q')){ document.getElementById('byoq').value=P.get('q');
    const g=(P.get('g')||'').split('.').filter(x=>GADD[x]);
    if(g.length){ byoAff=g; paintTags(); runByo(); } else submitByo();
    document.querySelector('.byos').scrollIntoView({block:'start'}); }
  else render("아이돌기획사" in ST ? "아이돌기획사" : Object.keys(ST)[0]);
})();
</script>'''

# 도메인 별칭 → 세팅키 (34세팅의 손검증 affords를 상속시켜 구체 명사 입력을 태깅)
_ALIAS={
 "스타트업":["스타트업","창업","벤처","테크기업","유니콘","액셀러레이터"],
 "대기업사내정치":["대기업","사내정치","그룹사","재벌","계열사","오너일가","임원","이사회"],
 "로펌":["로펌","변호사","법무법인","로스쿨","송무","변호","법률사무소"],
 "증권가":["증권","주식","투자은행","헤지펀드","트레이더","여의도","애널리스트","펀드매니저"],
 "방송국":["방송국","보도국","언론사","기자","뉴스룸","앵커","취재","신문사","데스크"],
 "아이돌기획사":["아이돌","연습생","기획사","보이그룹","걸그룹","케이팝","데뷔조","소속사","멤버"],
 "공직":["국회","공직","정치인","의원","시장","선거","청와대","정부","관가","보좌관","인턴"],
 "종합병원":["병원","응급실","의사","외과","전공의","수술","간호사","의료","의대","레지던트","닥터"],
 "군대":["군대","부대","병영","소대","군인","이등병","병장","훈련소","연대","사단","입대"],
 "교도소":["교도소","감옥","수감","재소자","죄수","교정","형무소","감방"],
 "요양원":["요양원","요양병원","실버타운","간병","호스피스","요양"],
 "사이비공동체":["사이비","종교","교단","교주","신도","공동체","컬트","사원","광신"],
 "대학원연구실":["대학원","연구실","랩실","교수","조교","논문","석박사","연구팀","실험실"],
 "요리경연":["요리","셰프","레스토랑","주방","파인다이닝","미슐랭","다이닝","쿡"],
 "프로스포츠팀":["스포츠","구단","프로팀","선수","감독","리그","야구","축구","경기장"],
 "오디션서바이벌":["오디션","서바이벌","경연","참가자","서바","심사","서바이벌프로"],
 "프로게임단":["e스포츠","이스포츠","게임단","프로게이머","롤","게이밍","프로게임","옵치","발로란트"],
 "재개발조합":["재개발","재건축","조합","세입자","철거","분양","입주","용역"],
 "셰어하우스":["셰어하우스","하우스메이트","셰어","룸메","쉐어","공동주거"],
 "스트리머판":["스트리머","유튜버","인플루언서","크리에이터","방송인","bj","틱톡","채널","구독자","웹툰","만화"],
 "긱이코노미":["배달","라이더","택배","물류센터","물류","배달앱","대리","플랫폼노동","쿠팡","편의점","알바","아르바이트"],
 "재혼가정":["재혼","새엄마","계모","의붓","이복","새아빠"],
 "코인판":["코인","크립토","비트코인","블록체인","nft","러그풀","암호화폐","알트코인","디파이","중고차","딜러","흥정"],
 "AI연구소":["ai","인공지능","머신러닝","알고리즘","챗봇","llm","딥러닝","연구소"],
 "콘텐츠검열팀":["검열","신뢰안전","모더레이션","모더레이터","신고","콘텐츠정책","필터링"],
 "팬데믹대응팀":["팬데믹","감염","방역","역학","질본","전염병","격리소","방역팀"],
 "우주기업":["우주","우주선","정거장","화물선","우주비행","심해","시추선","시추","선장","크루","항해사"],
 "귀농귀향":["귀농","귀향","시골","고향","농촌","산골","전원"],
 "케이퍼":["케이퍼","사기단","하이스트","강도","절도","도둑","한탕","금고","털이"],
 "재난현장":["재난","지진","붕괴","참사","구조대","화재","침몰","산사태","구조대원"],
 "셀럽판":["셀럽","연예인","스타","배우","파파라치","스캔들","가수","톱스타","연예계","성형"],
 "가상세계":["메타버스","게임세계","이세계","가상현실","아바타","디지털세계"],
 "신분세탁":["신분세탁","사칭","리플리","위조신분","상류","계급상승","가짜신분"],
 "부당수용":["부당수용","정신병원","억울","누명","수용소","강제입원","오진"],
}
DOM={a:k for k,al in _ALIAS.items() if k in st for a in al}
out=(T.replace("__SK__", json.dumps(sk,ensure_ascii=False))
      .replace("__ST__", json.dumps(st,ensure_ascii=False))
      .replace("__GL__", json.dumps(GL,ensure_ascii=False))
      .replace("__PR__", json.dumps(pr,ensure_ascii=False))
      .replace("__CS__", json.dumps(cs,ensure_ascii=False))
      .replace("__CTOT__", str(cmeta.get("total",0)))
      .replace("__CNS__", str(cmeta.get("n_settings",0)))
      .replace("__NSET__", str(len(st)))
      .replace("__FEAT__", json.dumps(["아이돌기획사","우주기업","AI연구소","코인판","셰어하우스"],ensure_ascii=False))
      .replace("__DOM__", json.dumps(DOM,ensure_ascii=False)))
open(f"{ROOT}/exhibits/match-explorer.html","w",encoding="utf-8").write(out)
print("match-explorer.html", len(out), "bytes ·", len(sk),"skeletons ·",len(st),"settings")
