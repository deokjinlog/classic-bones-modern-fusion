# 「센터」 작화 발주서 (art prompt pack)

외부 이미지 모델(Midjourney / NijiJourney / SDXL 등)로 웹툰 컷을 뽑기 위한 프롬프트 팩.
뽑은 이미지를 `exhibits/center-webtoon.html`의 벡터 자리에 얹으면 완성형 웹툰이 됨.

## 1) 스타일 락 (모든 프롬프트 앞에 붙이기)
```
korean webtoon / manhwa illustration, full color, clean cel shading, bold rim lighting,
cinematic K-pop stage, dramatic emotional mood, vertical webtoon panel, high detail
```
- **비율**: 세로 `--ar 3:4` (또는 2:3). NijiJourney면 `--niji 6`.
- **네거티브**: `text, watermark, extra fingers, deformed hands, low quality, jpeg artifacts`
- **일관성**: 캐릭터 참조(`--cref` / character sheet)를 매 컷에 고정 → 얼굴 안 흔들림.

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
이미지 모델은 한글 텍스트를 못 그리니 **작화는 텍스트 없이 뽑고**, 말풍선/대사는 나중에 합성.
현재 에피소드 대사는 `exhibits/center-webtoon.html` 참고.
