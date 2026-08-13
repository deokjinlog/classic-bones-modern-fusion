#!/usr/bin/env python3
"""exhibits/*.html(아티팩트용·wrapper 없음)을 GitHub Pages용 독립 HTML로 감싼다.
루트 index.html = 「센터」 웹툰 (레포 주소 상단바 포함).
사용: python3 src/build_pages.py
"""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = open(f"{ROOT}/exhibits/center-webtoon.html", encoding="utf-8").read()

bar = (
    '<div style="position:sticky;top:0;z-index:99;display:flex;gap:14px;align-items:center;'
    'justify-content:center;padding:9px 14px;background:#0b0b12;border-bottom:1px solid #242230;'
    'font:600 12.5px system-ui,sans-serif;color:#928ca1">'
    '<span style="color:#f6c453">classic-bones-modern-fusion</span>'
    '<span style="color:#5f5a6d">·</span>'
    '<a href="https://github.com/deokjinlog/classic-bones-modern-fusion" '
    'style="color:#ff2e88;text-decoration:none">GitHub 소스 →</a></div>'
)

html = (
    "<!doctype html>\n<html lang=\"ko\">\n<head>\n"
    "<meta charset=\"utf-8\">\n"
    "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
    "<title>센터 · classic-bones-modern-fusion</title>\n"
    "<meta name=\"description\" content=\"고전 햄릿의 뼈대를 아이돌 기획사에 이식해 조준·생성한 웹툰 에피소드.\">\n"
    "</head>\n<body style=\"margin:0;background:#08080e\">\n"
    + bar + "\n" + src + "\n</body>\n</html>\n"
)
open(f"{ROOT}/index.html", "w", encoding="utf-8").write(html)
print("index.html 생성 (", len(html), "bytes )")
