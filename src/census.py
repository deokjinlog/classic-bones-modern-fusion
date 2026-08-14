#!/usr/bin/env python3
"""census.py — WikiPlots(11만편 실제 이야기)에서 각 세팅 도메인이 몇 편에 나오는지 실측.
'이 도메인이 픽션에 얼마나 쓰였나'를 세어 신선도의 근거로 쓴다(추정치 modern_done을 뒷받침).
결과 → data/census.json. 코퍼스는 영어라 절대수치보다 상대 순위로 해석.
사용: python3 src/census.py
"""
import re, json, os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLOTS=f"{ROOT}/data/corpus/wikiplots/plots"

# 세팅키 → 영어 도메인 키워드 (WikiPlots가 영어라)
DOM={
 "스타트업":r"start-?up|tech company|silicon valley|venture capital",
 "대기업사내정치":r"corporation|corporate|conglomerate|boardroom|chief executive",
 "로펌":r"law firm|lawyer|attorney|litigation|legal case",
 "증권가":r"wall street|stockbroker|investment bank|hedge fund|trader",
 "방송국":r"newsroom|journalist|broadcast|television station|reporter|anchorman",
 "아이돌기획사":r"idol|k-?pop|boy band|girl group|pop star|music agency",
 "공직":r"politician|senator|congressman|governor|election campaign|mayor",
 "종합병원":r"hospital|surgeon|physician|medical staff|nurse|emergency room",
 "군대":r"army|military|soldier|platoon|barracks|regiment|battalion",
 "교도소":r"prison|inmate|jail|penitentiary|convict|cell block",
 "요양원":r"nursing home|retirement home|elderly care|assisted living",
 "사이비공동체":r"\bcult\b|sect|commune|guru|doomsday|charismatic leader",
 "대학원연구실":r"graduate student|laboratory|research team|professor|dissertation|thesis",
 "요리경연":r"cooking competition|chef|culinary|restaurant kitchen|cook-off",
 "프로스포츠팀":r"sports team|athlete|championship|coach|league|tournament",
 "오디션서바이벌":r"audition|talent show|reality (show|competition)|contestant",
 "프로게임단":r"esports|gaming team|video game (tournament|competition)|pro gamer",
 "재개발조합":r"redevelopment|urban renewal|tenant|eviction|gentrification",
 "셰어하우스":r"roommate|housemate|shared (house|apartment)|flatmate",
 "스트리머판":r"streamer|youtuber|influencer|content creator|internet celebrity|vlogger",
 "긱이코노미":r"delivery (driver|man)|courier|rideshare|gig (work|economy)|freelancer",
 "재혼가정":r"stepmother|stepfather|stepfamily|remarriage|blended family|stepchild",
 "코인판":r"cryptocurrency|bitcoin|\bcrypto\b|blockchain|\bnft\b",
 "AI연구소":r"artificial intelligence|\bA\.?I\.? (lab|research)|machine learning|sentient (computer|robot)",
 "콘텐츠검열팀":r"content moderation|censorship|moderator|misinformation",
 "팬데믹대응팀":r"pandemic|epidemic|outbreak|\bvirus\b|quarantine|plague",
 "우주기업":r"spaceship|spacecraft|space station|cargo ship|astronaut|deep space",
 "귀농귀향":r"returns? to (his|her|their) (home ?town|village)|rural|countryside|homecoming",
 "케이퍼":r"\bheist\b|con artist|robbery|con man|swindle|caper",
 "재난현장":r"disaster|earthquake|building collapse|trapped survivors?|catastrophe",
 "셀럽판":r"celebrity|famous (actor|singer|star)|tabloid|paparazzi|stardom",
 "가상세계":r"virtual reality|video game world|simulation|trapped in a game|\bVR\b",
 "신분세탁":r"impostor|false identity|social climber|passes? himself off|assumes? the identity",
 "부당수용":r"wrongful(ly)? (committed|confined|imprisoned)|insane asylum|falsely accused|institution",
}

txt=open(PLOTS,encoding="utf-8",errors="ignore").read()
stories=txt.split("<EOS>")
N=len(stories)
pats={k:re.compile(v,re.I) for k,v in DOM.items()}
counts={k:0 for k in DOM}
for s in stories:
    for k,rx in pats.items():
        if rx.search(s): counts[k]+=1

# 순위(희소할수록 신선) : 등장 적은 순
ranked=sorted(DOM, key=lambda k:counts[k])
rankpos={k:i+1 for i,k in enumerate(ranked)}
out={"_meta":{"corpus":"WikiPlots","total":N,"n_settings":len(DOM),
     "note":"세팅 도메인이 실제 이야기 몇 편에 나오나. 희소할수록 미개척(신선). 영어 코퍼스라 상대 순위로 해석."},
     "settings":{k:{"n":counts[k],"pct":round(counts[k]/N*100,3),"rarity_rank":rankpos[k]} for k in DOM}}
json.dump(out,open(f"{ROOT}/data/census.json","w",encoding="utf-8"),ensure_ascii=False,indent=0)
print(f"census 완료: {N}편 · {len(DOM)}세팅 → data/census.json")
for k in ranked:
    print(f"  {rankpos[k]:2d}. {k:14s} {counts[k]:6d}편 ({counts[k]/N*100:.2f}%)")
