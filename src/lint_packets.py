#!/usr/bin/env python3
"""lint_packets.py — 패킷 품질 게이트(결정적 불변식). LLM 없이, 골든 스키마 없이.
정답은 매 건에 있다 = 그 세팅의 #1 뼈대(구조). 그 구조 대비 불변식을 검사한다.
(폼 충실도 검증의 스토리판 — per-instance ground truth = 뼈대)

검사: ① 프리셋마다 패킷 있나 ② 필드 9개 다 채워졌나 ③ 전개 비트 수 == 뼈대 turns 수
      ④ 인물 수 == 뼈대 roles 수 ⑤ 반전(tw)이 자리 표시자/빈값 아닌가
CI에 붙여 프롬프트·데이터 회귀를 자동 검출. 사용: python3 src/lint_packets.py
"""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def load(p): return json.load(open(f"{ROOT}/data/{p}", encoding="utf-8"))
S, SK, P = load("settings.json"), load("skeletons.json"), load("premises.json")
sets = {k: v for k, v in S.items() if k != "_note"}
sks  = {k: v for k, v in SK.items() if k != "_note"}
FIELDS = ["p", "l", "c", "a", "rm", "hk", "tw", "th", "wn"]

def top_skeleton(aff):
    """세팅의 #1 뼈대 = 요구⊆보유 중 신선도×검증도 최고."""
    best, bs = None, -1
    for kn, sk in sks.items():
        if set(sk["req"]) - set(aff):
            continue
        sc = sk["proven"] * (1 - sk.get("modern_done", 0))
        if sc > bs:
            best, bs = kn, sc
    return best

issues = []
for key, st in sets.items():
    aff = st["affords"]
    pk = P.get(key)
    if pk is None:
        issues.append((key, "패킷 없음")); continue
    for f in FIELDS:                                   # ② 필드 완비
        v = pk.get(f)
        if v is None or (isinstance(v, (str, list)) and len(v) == 0):
            issues.append((key, f"필드 비었음: {f}"))
    top = top_skeleton(aff)
    if not top:
        issues.append((key, "적합 뼈대 없음")); continue
    turns, roles = sks[top].get("turns", []), sks[top].get("roles", [])
    if isinstance(pk.get("a"), list) and len(pk["a"]) != len(turns):   # ③ 전개==turns
        issues.append((key, f"전개 {len(pk['a'])}비트 ≠ 뼈대 turns {len(turns)} ({top})"))
    if isinstance(pk.get("rm"), list) and len(pk["rm"]) != len(roles):  # ④ 인물==roles
        issues.append((key, f"인물 {len(pk['rm'])} ≠ 뼈대 roles {len(roles)} ({top})"))
    tw = (pk.get("tw") or "").strip()                                  # ⑤ 반전 실체
    if tw and (len(tw) < 8 or set(tw) <= set("★☆*·-—.: ")):
        issues.append((key, "반전(tw)이 빈껍데기/기호"))

print(f"lint_packets — {len(sets)}세팅 검사 · 불변식: 필드9·전개==turns·인물==roles·반전실체")
if not issues:
    print("✅ 통과 — 모든 패킷이 자기 뼈대 구조에 충실"); sys.exit(0)
print(f"❌ {len(issues)}건 위반:")
for key, msg in issues:
    print(f"  · {key}: {msg}")
sys.exit(1)
