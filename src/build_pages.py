#!/usr/bin/env python3
"""exhibits/*.html(아티팩트용·wrapper 없음)을 GitHub Pages용 독립 HTML로 감싼다.
  index.html   = 매칭 성좌 (인터랙티브 랜딩, 자체 네비 → 바 없음)
  center.html  = 웹툰 「센터」
  cargo.html   = 웹툰 「화물」
  explore.html = 매칭 탐색기
성좌 외 페이지는 상단바로 상호 + 성좌 홈 + GitHub 크로스링크.
사용: python3 src/build_pages.py
"""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GH = "https://github.com/deokjinlog/classic-bones-modern-fusion"

def bar(nav):
    links = "".join(
        f'<span style="color:#5f5a6d">·</span>'
        f'<a href="{href}" style="color:#ff2e88;text-decoration:none">{label}</a>'
        for label, href in nav)
    return (
        '<div style="position:sticky;top:0;z-index:99;display:flex;gap:14px;align-items:center;'
        'justify-content:center;flex-wrap:wrap;padding:9px 14px;background:#0b0b12;border-bottom:1px solid #242230;'
        'font:600 12.5px system-ui,sans-serif;color:#928ca1">'
        '<span style="color:#f6c453">classic-bones-modern-fusion</span>' + links + '</div>')

def wrap(exhibit, title, desc, nav=None):
    src = open(f"{ROOT}/exhibits/{exhibit}", encoding="utf-8").read()
    head = (
        "<!doctype html>\n<html lang=\"ko\">\n<head>\n<meta charset=\"utf-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
        f"<title>{title}</title>\n<meta name=\"description\" content=\"{desc}\">\n"
        "</head>\n<body style=\"margin:0;background:#07060e\">\n")
    return head + (bar(nav) + "\n" if nav else "") + src + "\n</body>\n</html>\n"

pages = {
    "index.html": wrap("match-explorer.html", "매칭 탐색기 · classic-bones-modern-fusion",
        "세팅을 고르면 어떤 고전 뼈대가 맞는지·왜인지를 결정적으로 계산하는 인터랙티브 도구.",
        [("웹툰 「센터」 →", "center.html"), ("웹툰 「화물」 →", "cargo.html"), ("웹툰 「장부」 →", "coin.html"), ("방법론 →", "method.html"), ("GitHub →", GH)]),
    "center.html": wrap("center-webtoon.html", "센터 · classic-bones-modern-fusion",
        "고전 햄릿의 뼈대를 아이돌 기획사에 이식해 조준·생성한 웹툰 에피소드.",
        [("매칭 탐색기 →", "./"), ("웹툰 「화물」 →", "cargo.html"), ("웹툰 「장부」 →", "coin.html"), ("방법론 →", "method.html"), ("GitHub →", GH)]),
    "cargo.html": wrap("cargo-webtoon.html", "화물 · classic-bones-modern-fusion",
        "고전 오디세이의 뼈대를 우주 운송선에 이식해 조준·생성한 웹툰 에피소드.",
        [("매칭 탐색기 →", "./"), ("웹툰 「센터」 →", "center.html"), ("웹툰 「장부」 →", "coin.html"), ("방법론 →", "method.html"), ("GitHub →", GH)]),
    "coin.html": wrap("coin-webtoon.html", "장부 · classic-bones-modern-fusion",
        "고전 조사 미스터리(오이디푸스형)의 뼈대를 코인판에 이식해 조준·생성한 웹툰 에피소드.",
        [("매칭 탐색기 →", "./"), ("웹툰 「센터」 →", "center.html"), ("웹툰 「화물」 →", "cargo.html"), ("방법론 →", "method.html"), ("GitHub →", GH)]),
    "method.html": wrap("method.html", "만드는 법 · classic-bones-modern-fusion",
        "결정적 매칭·근거·6레버 깊이 — 이 도구가 어떻게 작동하는지의 메이킹 문서.",
        [("매칭 탐색기 →", "./"), ("웹툰 「센터」 →", "center.html"), ("웹툰 「화물」 →", "cargo.html"), ("웹툰 「장부」 →", "coin.html"), ("GitHub →", GH)]),
}
for name, html in pages.items():
    open(f"{ROOT}/{name}", "w", encoding="utf-8").write(html)
    print(name, len(html), "bytes")
