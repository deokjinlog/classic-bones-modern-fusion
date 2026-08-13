#!/usr/bin/env python3
"""render_art.py — 우리 발주서(data/art_shots.json)로 Gemini 2.5 Flash Image(나노바나나)를
호출해 assets/art/<id>.png 를 자동 생성한다. 웹툰은 그 PNG가 있으면 진짜 작화를,
없으면 SVG 장면을 자동 표시(폴백). = "연출은 우리 파이프라인, 렌더는 이미지 모델".

무료 키 발급 : https://aistudio.google.com/apikey
설치        : pip install google-genai
실행        : export GEMINI_API_KEY=...   &&   python3 src/render_art.py [all|center|cargo]
반영        : 로컬은 즉시. GitHub Pages에 올리려면 assets/art/*.png 를 커밋.
"""
import os, sys, json, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEY = os.environ.get("GEMINI_API_KEY")
if not KEY:
    sys.exit("GEMINI_API_KEY 없음.\n  무료 키: https://aistudio.google.com/apikey\n"
             "  pip install google-genai\n  export GEMINI_API_KEY=...\n  python3 src/render_art.py")

try:
    from google import genai
    from google.genai import types
except ImportError:
    sys.exit("google-genai 미설치 → pip install google-genai")

which = sys.argv[1] if len(sys.argv) > 1 else "all"
data = json.load(open(f"{ROOT}/data/art_shots.json", encoding="utf-8"))
style = data.get("style", "")
shots = [s for s in data["shots"] if which in ("all", s["webtoon"])]
os.makedirs(f"{ROOT}/assets/art", exist_ok=True)

client = genai.Client(api_key=KEY)
anchor = {}   # webtoon -> 첫 컷 이미지 bytes (캐릭터/스타일 앵커)

def one(shot):
    out = f"{ROOT}/assets/art/{shot['id']}.png"
    text = (style + ". " if style else "") + shot["prompt"]
    contents = [text]
    ref = anchor.get(shot["webtoon"])
    if ref:  # 같은 웹툰의 앞 컷을 레퍼런스로 → 캐릭터·화풍 유지
        contents = ["Keep the same character(s), face, outfit and art style as the reference image. " + text,
                    types.Part.from_bytes(data=ref, mime_type="image/png")]
    cfg = types.GenerateContentConfig(
        response_modalities=["IMAGE"],
        image_config=types.ImageConfig(aspect_ratio=shot.get("aspect", "16:9")),
    )
    resp = client.models.generate_content(model="gemini-2.5-flash-image", contents=contents, config=cfg)
    for part in resp.parts:
        if getattr(part, "inline_data", None) and part.inline_data.data:
            img = part.inline_data.data
            open(out, "wb").write(img)
            anchor.setdefault(shot["webtoon"], img)
            return len(img)
    raise RuntimeError("응답에 이미지 없음 (안전필터/쿼터 확인)")

ok = 0
for s in shots:
    for attempt in range(1, 5):
        try:
            n = one(s); print(f"  ✓ {s['id']}  ({n//1024} KB)"); ok += 1; break
        except Exception as e:
            print(f"  · {s['id']} 시도 {attempt} 실패: {e}")
            time.sleep(8)
    time.sleep(3)  # 무료 쿼터 배려

print(f"\n완료 {ok}/{len(shots)} → assets/art/")
print("웹툰(center.html·cargo.html)이 자동으로 진짜 작화를 표시합니다. (없는 컷은 SVG 유지)")
print("Pages 반영: git add assets/art && commit && push")
