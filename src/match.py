#!/usr/bin/env python3
"""결정적 매칭 엔진 v0 — 세팅 하나에 어느 뼈대가 맞나 순위.
매칭은 하드게이트(요구 ⊆ 보유)로만. 취향 0, 재현됨.
사용: python3 src/match.py 아이돌기획사
"""
import json, sys, math, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SK = {k: v for k, v in json.load(open(f"{ROOT}/data/skeletons.json", encoding="utf-8")).items() if not k.startswith("_")}
ST = {k: v for k, v in json.load(open(f"{ROOT}/data/settings.json", encoding="utf-8")).items() if not k.startswith("_")}


def rank(setting_key):
    affords = set(ST[setting_key]["affords"])
    rows = []
    for k, s in SK.items():
        req = set(s["req"])
        met = req & affords
        rate = len(met) / len(req) if req else 0
        fresh = 1 - s.get("modern_done", 0.5)          # 집거리 대용: 현대로 덜 옮겨졌을수록 신선
        score = fresh * s["freq"] if rate >= 0.999 else 0  # 완전 적합만 후보
        rows.append({"name": s["name"], "rate": rate, "met": len(met), "tot": len(req),
                     "freq": s["freq"], "fresh": round(fresh, 2), "score": round(score, 1),
                     "missing": sorted(req - affords)})
    rows.sort(key=lambda r: (-r["score"], -r["rate"]))
    return rows


def main():
    key = sys.argv[1] if len(sys.argv) > 1 else "아이돌기획사"
    st = ST[key]
    print(f"■ 세팅: {st['name']}   보유: {st['affords']}")
    print(f"  ({st['gloss']})\n")
    print("  점수 = 신선도(1−현대소진) × 빈도  [완전 적합만]")
    print("  " + "-" * 68)
    for r in rank(key):
        if r["score"] > 0:
            print(f"  ✅ {r['score']:>5}  충족 {r['met']}/{r['tot']} · 신선 {r['fresh']} · 빈도 {r['freq']:>2}  {r['name']}")
    print("  " + "-" * 68 + "  (아래=부적합/부분)")
    for r in rank(key):
        if r["score"] == 0:
            mark = "🔸" if r["rate"] >= 0.5 else "❌"
            miss = f"  [부족: {','.join(r['missing'])}]" if r["missing"] else ""
            print(f"  {mark} 충족 {r['met']}/{r['tot']}  {r['name']}{miss}")


if __name__ == "__main__":
    main()
