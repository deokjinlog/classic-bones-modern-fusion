#!/usr/bin/env python3
"""render_art.py — 우리 발주서(data/art_shots.json)로 컷을 자동 생성 → assets/art/<id>.png.
웹툰은 PNG 있으면 진짜 작화, 없으면 SVG 자동 표시(폴백).
= "연출·조준·조립은 우리 파이프라인, 렌더 픽셀만 이미지 모델에 호출".

백엔드(자동 선택):
  • GEMINI_API_KEY 있으면 → Gemini 2.5 Flash Image(나노바나나). 웹툰체·얼굴 일관성 최상. 단 API는 유료(무료 티어=0).
  • 없으면            → Pollinations(Flux). 무료·키 없음·자동. 반실사 애니톤, 컷별 일관성은 약함.

의존성 0 (표준 라이브러리만).
실행 : python3 src/render_art.py [all|center|cargo]
반영 : 로컬 즉시. GitHub Pages엔 assets/art/*.png 커밋.
"""
import os, sys, json, time, base64, urllib.request, urllib.parse, urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEY = os.environ.get("GEMINI_API_KEY")
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36", "Accept": "image/*"}

def gen_gemini(prompt, aspect, ref_b64, seed):
    api = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent"
    parts = [{"text": prompt}]
    if ref_b64:
        parts.append({"inlineData": {"mimeType": "image/png", "data": ref_b64}})
    body = {"contents": [{"parts": parts}],
            "generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": aspect}}}
    req = urllib.request.Request(api, data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "x-goog-api-key": KEY})
    with urllib.request.urlopen(req, timeout=180) as r:
        d = json.load(r)
    for c in d.get("candidates", []):
        for p in c.get("content", {}).get("parts", []):
            inl = p.get("inlineData") or p.get("inline_data")
            if inl and inl.get("data"):
                return base64.b64decode(inl["data"])
    raise RuntimeError("Gemini 응답에 이미지 없음: " + json.dumps(d)[:200])

ILLUS = "korean webtoon style illustration, cinematic lighting, no text. "
def gen_pollinations(prompt, aspect, ref_b64, seed):
    url = ("https://image.pollinations.ai/prompt/" + urllib.parse.quote(ILLUS + prompt) +
           f"?width=1024&height=640&nologo=true&referrer=classicbones&seed={seed}")
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=180) as r:
        return r.read()

BACKEND = ("Gemini(나노바나나)", gen_gemini) if KEY else ("Pollinations(무료)", gen_pollinations)
print(f"백엔드: {BACKEND[0]}")

which = sys.argv[1] if len(sys.argv) > 1 else "all"
data = json.load(open(f"{ROOT}/data/art_shots.json", encoding="utf-8"))
style = data.get("style", "")
shots = [s for s in data["shots"] if which in ("all", s["webtoon"])]
os.makedirs(f"{ROOT}/assets/art", exist_ok=True)
anchor, ok = {}, 0

for i, s in enumerate(shots):
    text = (style + ". " if style else "") + s["prompt"]
    ref = anchor.get(s["webtoon"]) if KEY else None
    if ref:
        text = "Keep the same recurring character(s) — same face, hair, outfit — and same art style as the reference image. " + text
    for attempt in range(1, 4):
        try:
            img = BACKEND[1](text, s.get("aspect", "16:9"), ref, i + 7)
            open(f"{ROOT}/assets/art/{s['id']}.png", "wb").write(img)
            if KEY:
                anchor.setdefault(s["webtoon"], base64.b64encode(img).decode())
            print(f"  ✓ {s['id']}  ({len(img)//1024} KB)"); ok += 1; break
        except Exception as e:
            print(f"  · {s['id']} 시도 {attempt} 실패: {str(e)[:140]}"); time.sleep(6)
    time.sleep(1)

print(f"\n완료 {ok}/{len(shots)} → assets/art/  (웹툰이 자동으로 진짜 작화 표시)")
