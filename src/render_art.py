#!/usr/bin/env python3
"""render_art.py — 우리 발주서(data/art_shots.json)로 Gemini 2.5 Flash Image(나노바나나)를
REST로 호출해 assets/art/<id>.png 를 자동 생성. 의존성 0(파이썬 표준 라이브러리만).
웹툰은 PNG 있으면 진짜 작화, 없으면 SVG 자동 표시(폴백).
= "연출·조준·조립은 우리 파이프라인, 렌더 픽셀만 이미지 모델에 호출".

무료 키 : https://aistudio.google.com/apikey  (결제 미연결이면 과금 자체가 불가 — 안 되면 그냥 에러)
실행    : export GEMINI_API_KEY=...  &&  python3 src/render_art.py [all|center|cargo]
반영    : 로컬 즉시. GitHub Pages엔 assets/art/*.png 커밋하면 반영.
"""
import os, sys, json, time, base64, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEY = os.environ.get("GEMINI_API_KEY")
if not KEY:
    sys.exit("GEMINI_API_KEY 없음.\n  무료 키: https://aistudio.google.com/apikey\n  export GEMINI_API_KEY=...\n  python3 src/render_art.py")

MODEL = os.environ.get("ART_MODEL", "gemini-2.5-flash-image")
API = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"

def gen(prompt, aspect, ref_b64=None):
    parts = [{"text": prompt}]
    if ref_b64:
        parts.append({"inlineData": {"mimeType": "image/png", "data": ref_b64}})
    body = {"contents": [{"parts": parts}],
            "generationConfig": {"responseModalities": ["IMAGE"],
                                 "imageConfig": {"aspectRatio": aspect}}}
    req = urllib.request.Request(API, data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "x-goog-api-key": KEY})
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            d = json.load(r)
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP {e.code}: {e.read().decode()[:300]}")
    for c in d.get("candidates", []):
        for p in c.get("content", {}).get("parts", []):
            inl = p.get("inlineData") or p.get("inline_data")
            if inl and inl.get("data"):
                return inl["data"]  # base64 str
    raise RuntimeError("응답에 이미지 없음: " + json.dumps(d)[:300])

which = sys.argv[1] if len(sys.argv) > 1 else "all"
data = json.load(open(f"{ROOT}/data/art_shots.json", encoding="utf-8"))
style = data.get("style", "")
shots = [s for s in data["shots"] if which in ("all", s["webtoon"])]
os.makedirs(f"{ROOT}/assets/art", exist_ok=True)
anchor = {}  # webtoon -> 첫 컷 base64 (캐릭터·화풍 앵커)
ok = 0

for s in shots:
    text = (style + ". " if style else "") + s["prompt"]
    ref = anchor.get(s["webtoon"])
    if ref:
        text = "Keep the same recurring character(s) — same face, hair, outfit — and the same art style as the reference image. " + text
    for attempt in range(1, 5):
        try:
            b64 = gen(text, s.get("aspect", "16:9"), ref)
            open(f"{ROOT}/assets/art/{s['id']}.png", "wb").write(base64.b64decode(b64))
            anchor.setdefault(s["webtoon"], b64)
            print(f"  ✓ {s['id']}  ({len(b64)*3//4//1024} KB)"); ok += 1; break
        except Exception as e:
            print(f"  · {s['id']} 시도 {attempt} 실패: {e}")
            time.sleep(8)
    time.sleep(2)

print(f"\n완료 {ok}/{len(shots)} → assets/art/")
print("웹툰이 자동으로 진짜 작화 표시(없는 컷은 SVG). Pages 반영: git add assets/art && commit")
