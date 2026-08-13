# 「센터」 작화 발주서 (art prompt pack)

외부 이미지 모델로 웹툰 컷을 뽑기 위한 프롬프트 팩. 뽑은 이미지를 `exhibits/center-webtoon.html`의
벡터 자리에 얹으면 완성형 웹툰이 됨. **텍스트 없이** 그림만 뽑으면 됨(말풍선은 후작업).

## 0) 실행 순서 (이대로만 하면 됨)
1. 아래 **① 스타일 락**을 복사해 매 프롬프트 맨 앞에 붙인다.
2. 먼저 **캐릭터 시트**부터 뽑아 서하·도경 얼굴을 **확정**한다(일관성 기준점).
   - 미드저니/니지면 그 이미지를 `--cref <이미지URL>`로 각 컷에 물린다 → 얼굴 안 흔들림.
   - 무료툴이면 같은 대화 세션에서 "same character as the previous image"로 이어 뽑는다.
3. **③ 패널 프롬프트 6컷**을 하나씩 뽑는다(세로 3:4).
4. 6장 나오면 **나한테 이미지(파일/URL) 주면** 벡터 자리에 얹어 완성형으로 조립한다.

**툴 선택**
| 툴 | 비용 | 웹툰 적합 | 일관성 |
|---|---|---|---|
| **Nano Banana (Gemini 2.5 Flash Image)** | **무료권** | ★★★ | **최강** — 캐릭터·구도 유지하며 편집 |
| NijiJourney 6 | 유료 | ★★★ (애니/웹툰 특화) | `--cref` 강력 |
| Midjourney v6 | 유료 | ★★ | `--cref` 강력 |
| ChatGPT(DALL·E 3)·Bing | 무료권 | ★★ | 세션 내 "same character"로 유지 |

> **추천: Nano Banana(Gemini)부터.** 무료 + 캐릭터 일관성·부분수정이 웹툰에 최적. **한 컷 먼저 뽑아 붙여보고** 될지 판단 → 되면 나머지.

## 1) 스타일 락 (모든 프롬프트 앞에 붙이기)
```
korean webtoon / manhwa illustration, full color, clean cel shading, bold rim lighting,
cinematic K-pop stage, dramatic emotional mood, vertical webtoon panel, high detail, no text
```
- **비율**: 세로 `--ar 3:4`. NijiJourney면 `--niji 6`.
- **네거티브**: `text, letters, watermark, extra fingers, deformed hands, low quality, jpeg artifacts`

## 2) 캐릭터 시트 (프롬프트마다 해당 인물 설명 고정)
- **서하**(주인공): 19yo Korean male K-pop trainee, black messy fringe partly over eyes, sharp shadowed intense gaze, oversized charcoal hoodie
- **도경**(찬탈자): 22yo Korean male idol center, ash-blonde swept-back hair, flawless white-and-silver stage outfit, cold confident smirk
- **서준**(형/사진): 서하를 닮은 22yo, brighter softer look — appears only in a framed photo
- **김 매니저**: 30s weary Korean man, short dark hair, navy suit, lanyard ID, tired eyes

## 3) 패널 프롬프트 (6컷)
```
① [찬탈] Empty grand K-pop stage, a single gold spotlight center. DOKYUNG (ash-blonde,
   white-silver stage outfit) walks into the light with a cold confident smirk, facing camera.
   In the dark background, a faint silhouette (SEOJUN) exits with his back turned. glamorous but chilling.

② [후계자] Dim idol company waiting room. SEOHA (black fringe, charcoal hoodie) alone,
   looking up at a glowing framed profile photo of his brother SEOJUN on the wall.
   magenta backlight, lonely, emotional close-up.

③ [유령] Pitch-dark practice room. A smartphone on the floor glows with a cyan audio waveform
   leaking out like a ghost. SEOHA kneels, hand reaching for the play button, eyes wide with shock.
   eerie cyan glow, high contrast.

④ [망설임] SEOHA alone, face split — left half in hot magenta light, right half in cold cyan light.
   torn, conflicted expression, extreme chiaroscuro, dramatic close-up.

⑤ [곁가지] Night hallway of the agency. KIM the manager carries a cardboard box, pausing to look
   back at SEOHA with a tired, knowing half-smile. light spilling from a doorway, melancholy.

⑥ [클라이맥스] Huge comeback live stage, gold spotlight. SEOHA at the mic, facing forward.
   Behind him, frozen idol member silhouettes; cyan audio waveform scatters in the air.
   cameras and crowd frozen. climax, wide dramatic shot.
```

## 4) 대사(말풍선)는 후작업으로 얹기
이미지 모델은 한글을 못 그리니 **작화는 텍스트 없이 뽑고**, 말풍선/대사는 나중에 합성.
현재 에피소드 대사·컷 순서는 `exhibits/center-webtoon.html` 참고.

## 5) 나한테 넘기는 법
6장(또는 일부)을 뽑으면 **파일 첨부 or 이미지 URL**로 주면 됨. 내가:
- 각 컷을 해당 패널의 벡터 자리에 교체(비율·크롭 맞춤)
- 말풍선·비트 캡션·근거 섹션은 그대로 유지
- 아티팩트 + GitHub Pages 재배포
