# 데이터 수확 보고서 — 실제로 받아서 까본 결과

> **2026-08-06 실행.** 4종 1.6GB 다운·압축해제·샘플 검증 완료. 각 데이터가 **실제로 뭘 주는지 + 로코 팩에 뭘 쓸지 판단**까지.
> 위치: `~/deokjinlog/story-rag/data/`

---

## 받은 것 (전부 실물 검증 ✅ — HTML 에러페이지 아님)

| 데이터 | 압축 | 해제 | 규모 | 라이선스 | 검증 |
|---|---|---|---|---|---|
| **WikiPlots** | 88M | 226M | 112,936 스토리·207만 문장 | CC-BY-SA ✅상업 | Animal Farm 줄거리 실물 |
| **TVTropes 풀** | 629M | ~2.3G | 트로프 216,685·발생 190만·40K작품 | CC-BY-NC ⚠️포폴 | 로코 트로프 7종 존재 확인 |
| **Goodreads 로맨스** | 348M | ~1.66G | 33.5만 권·리뷰 | 연구용 | popular_shelves 집계 성공 |
| **Goodreads 장르** | 24M | — | book_id→장르 매핑 | 연구용 | 매핑 실물 확인 |
| **AO3 메타** | 194M | 194M | 24 팬덤·관계·태그·Kudos | CC-BY-4.0 ✅재배포 | 컬럼 23종 확인 |

---

## 데이터별 실물 + 판단

### ① WikiPlots — 플롯 전개 원천
- **구조**: `titles`(제목) + `plots`(한 문장/줄, `<EOS>` 구분)
- **실물**: Animal Farm이 "Old Major가 소집 → 반란 → 7계명 → 권력투쟁…" 20줄 깔끔한 산문
- **판단**: ✅ 비트/전개 패턴 학습용, 파싱 쉬움, **상업 안전**. ⚠️ **장르 태그 없음** → 로코만 걸러내려면 제목→위키 카테고리 매칭 or LLM 분류 **전처리 1회 필요**.

### ② TVTropes 풀 — 트로프 접지 최강
- **구조**: `tropes.csv`(정의 21.6만) + `{film,tv,lit}_tropes.csv`(작품↔트로프+**실제 예시문장**) + `*_imdb_match`·`lit_goodreads_match`(인기 연결)
- **실물**: 로코 트로프 **7종 전부 존재** (MeetCute·FakeRelationship·OppositesAttract·BelligerentSexualTension·GrandRomanticGesture·SecondActBreakup·NotWhatItLooksLike)
- **판단**: ✅ 팩 ④ 트로프 슬롯의 **최강 접지**. 정의 + "이 작품에 이렇게 쓰임" 예시까지. IMDb/Goodreads 매칭으로 인기 가중 가능. ⚠️ **CC-BY-NC = 포폴 전용**(상업 전환 시 제외).

### ③ Goodreads 로맨스 — 인기·서브장르 신호 (실용 승자)
- **구조(JSON/권)**: `popular_shelves`(유저 태그) · `description`(블러브) · `average_rating` · `ratings_count` · `title` · `authors`
- **실물 집계(10만 권)**: 인기 태그 = contemporary-romance · historical-romance · paranormal-romance · chick-lit · new-adult · **m-m** · erotica · regency · urban-fantasy · vampires…
- **판단**: ✅ **서브장르·배경·톤 신호가 제일 실용적**(로맨스 특화 + 유저 실태그 + rating 인기가중). description은 "블러브 = 훅 쓰는 법" 학습 소스. ⚠️ **미시 트로프**(enemies-to-lovers·fake-dating)는 상위 밖 → 트로프 정밀도는 ②가 우위. 라이선스 연구용(포폴 OK, 상업은 확인).

### ④ Goodreads 장르 매핑 — 필터 보조
- **실물**: `{"book_id":"7327624","genres":{"fantasy, paranormal":31,"fiction":8,...}}`
- **판단**: ③를 장르로 거르는 보조 인덱스. 단독 가치는 낮음.

### ⑤ AO3 메타 — 관계 역학 신호 (한계 있음)
- **구조(23컬럼)**: Relationship·Characters·AdditionalTags·**Kudos·Hits·Bookmarks**(인기)·Words·Rating…
- **⚠️ 중요 발견**: **장르별이 아니라 팬덤별**(해리포터·마블·세일러문 등 24개). = **기존작 2차창작(팬픽)**이지 오리지널 로맨스 장르가 아님.
- **판단**: △ **관계 다이내믹 패턴 + 태그 공기(共起) + Kudos 인기 신호**엔 유용(큰 팬덤에서 관계별 kudos 집계 → "인기 관계 유형"). 단 **장르 컨벤션 직접 접지엔 간접적**. CC-BY-4.0(재배포 자유)는 장점.

---

## 종합 판단 — 로코 팩 슬롯별 데이터 배정

| 팩 슬롯 | 1순위 데이터 | 근거 |
|---|---|---|
| **② 관계 역학** | AO3 Kudos 집계 (+ Goodreads m-m/f-f 태그) | 인기 관계 유형 신호 |
| **③ 플롯 비트** | WikiPlots (로맨스 필터) | 전개 패턴 |
| **④ 트로프** | **TVTropes** (정의+예시) | 미시 트로프 정밀 |
| **⑤ 톤·서브장르** | **Goodreads popular_shelves + description** | 인기 서브장르·블러브 |
| **인기 가중** | Goodreads rating · AO3 Kudos · TVTropes-IMDb매칭 | "뭐가 먹히나" |

## 정직한 한계 3가지 (기획에 반영)
1. **어떤 것도 "로코 장르"를 바로 주진 않음** — WikiPlots(장르무태그)·AO3(팬덤)·Goodreads(로맨스 광의). **로코 필터/분류 전처리가 공통 관문.**
2. **Goodreads = 서브장르 강, 미시트로프 약 / TVTropes = 트로프 강, 인기신호 약** → **둘을 교차**해야 "인기 있는 트로프"가 나옴.
3. **상업 전환 시 TVTropes(NC)·AO3(팬픽) 빠짐** → WikiPlots+Goodreads(rating)만으로 축소 가능.

## 다음 단계 (판단 후)
- **A안**: Goodreads 로맨스에서 "로코/코미디" 하위필터 → popular_shelves·description으로 팩 ⑤⑥ 실데이터 접지 (제일 빠른 성과)
- **B안**: TVTropes 로코 트로프 클러스터 추출 → 팩 ④ 접지
- **C안**: 셋 다 로코 필터 → 통합 "로코 컨벤션 팩 v1" (본격)
