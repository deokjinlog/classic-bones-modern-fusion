# classic-bones-modern-fusion

[![검증된 고전 뼈대를 현대 세팅에 이식한다 — 세팅→매칭(코드)→융합(LLM)→프리미스+근거](assets/hero.png)](https://deokjinlog.github.io/classic-bones-modern-fusion/)

고전 이야기의 구조를 현대 배경에 옮겨서, 새롭지만 익숙한 이야기 소재를 만드는 도구.
어떤 구조가 어떤 배경에 맞는지는 실제 이야기 데이터로 계산하고, 프리미스 문장은 LLM이 쓴다.

## 바로 보기 (레포에서 바로 열림)

- 매칭 탐색기 (랜딩): https://deokjinlog.github.io/classic-bones-modern-fusion/
  세팅을 고르면 맞는 고전 뼈대와 그 근거, 프리미스를 보여준다.
- 웹툰 「센터」 (햄릿 × 아이돌): [center.html](https://deokjinlog.github.io/classic-bones-modern-fusion/center.html)
- 웹툰 「화물」 (오디세이 × 우주선): [cargo.html](https://deokjinlog.github.io/classic-bones-modern-fusion/cargo.html)

design-explosion의 스토리 버전. 모델에 "신선한 이야기 줘"라고 하면 대개 흔한 클리셰가 나오는데,
이 도구는 실제 이야기를 세어서 "이 조합이 덜 쓰였다"는 근거를 붙여준다. 무엇을 쓸지는 코드가 고르고, 문장은 LLM이 쓴다.

## 한눈에 — 세팅 하나 → 피칭 패킷

`아이돌 기획사`를 넣으면:

```
프리미스 : 창립 센터가 '자진 탈퇴'로 밀려난 뒤, 그 자리를 꿰찬 멤버가 팀을 독식한다.
           원조 센터의 동생인 신인이 삭제됐어야 할 녹취에서 퇴출 조작을 알아채지만,
           폭로하면 그룹이 죽는다. 망설이는 사이, 컴백 무대에서 모든 게 터진다.
comp    : 햄릿 meets 아이돌 서바이벌
로그라인 : 형의 자리를 뺏은 센터에게 복수하려는 신인이, 그 망설임으로 팀을 무너뜨린다.
근거    : 뼈대 검증 33 · 궁정→아이돌 이식 신선 · 요구 2/2 충족(G3·G9) · 이 세팅 1등 매칭
```

검증된 구조 위에 쓰니 백지보다 낫고, 아무도 안 한 조합이라 신선하고, 그게 왜 신선한지 숫자로 남는다.

## 어떻게 동작하나

세 가지 데이터 층으로 나눈다.

| 층 | 설명 | 출처 |
|---|---|---|
| 뼈대 | 이야기의 구조 (엔진·역할·턴). 찬탈복수 = 햄릿형 | WikiPlots에서 추출 |
| 스키마 | 뼈대가 요구하는 조건의 공통 어휘 (27) | 실제 이야기에서 도출 |
| 세팅 | 이식할 현대 무대 (스타트업·병원·아이돌 등) | 큐레이션 + 도메인 사실로 태깅 |

```
세팅 선택 → 매칭(요구 ⊆ 보유, 코드) → 융합(LLM) → 프리미스 + 근거
```

- 매칭은 집합 연산이라 재현·검수가 된다. 점수는 신선도 × 검증도.
- 프리미스는 LLM이 쓰지만, 구조는 뼈대가 고정한다.
- 스키마는 내용물(왕·검·궁정)이 아니라 조건(뺏을 권좌·밝혀질 살인)만 다룬다. 그래야 다른 세팅으로 옮겨진다.

## 왜 데이터를 세나

"신선한 걸 줘"라고 하면 모델은 학습에서 흔한 쪽으로 회귀한다. 무엇이 덜 쓰였는지는 세어보기 전엔 모른다.
이 도구의 값어치는 프리미스 자체보다, 그 조합이 실제로 덜 쓰였다는 근거에 있다.

## 써보기

프로젝트 폴더에서 스킬 `classic-bones-fusion`을 부르고 세팅 하나를 던지면 매칭 → 융합 → 패킷이 나온다.

```bash
python3 src/match.py 아이돌기획사   # 매칭만 미리 보기 (뼈대 순위)
```

규모: 뼈대 23종, 세팅 34종, 스키마 27속성. 모든 뼈대가 최소 하나의 세팅에 매칭된다.

## 레포 구조

| 경로 | 내용 |
|---|---|
| `docs/schema.md` | 스키마 27속성 (하드게이트/보편 조건/전개 태그) |
| `data/skeletons.json` · `data/settings.json` | 뼈대 23 · 세팅 34 |
| `data/premises.json` | 세팅별 피칭 패킷 (프리미스·로그라인·comp·전개) |
| `src/match.py` | 매칭 엔진 |
| `src/gen_explorer.py` · `src/build_pages.py` | 탐색기·페이지 생성 |
| `src/render_art.py` | 웹툰 작화 생성 (Gemini 또는 무료 Pollinations) |
| `.claude/skills/classic-bones-fusion/` | 스킬 |
| `exhibits/` · `index.html` | 탐색기·웹툰 (GitHub Pages) |

## 데이터 · 라이선스

- WikiPlots (CC-BY-SA) = 뼈대·스키마의 원석. TVTropes (CC-BY-NC) = 클리셰 회피용 참고.
- 코퍼스 본체는 `.gitignore`. 재다운 URL은 [`docs/data-sources.md`](docs/data-sources.md).
- 코드·문서 [MIT](LICENSE). 데이터는 각자 라이선스. 포트폴리오·비상업.
