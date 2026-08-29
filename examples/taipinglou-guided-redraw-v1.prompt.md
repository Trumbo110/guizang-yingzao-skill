# 太平楼排版垫图整体重绘 v1

本次使用内置 `imagegen` 的 `style-transfer` 编辑流程。输入为原照片和 [taipinglou-layout-guide-v2.png](taipinglou-layout-guide-v2.png)，没有进行生成后的文字回叠。

```text
Use case: style-transfer.
Asset type: 3:4 vertical contemporary Chinese architecture editorial travel poster.

Input images:
- Image 1 is the edit target and the sole source of the real Taiping Tower architecture, camera viewpoint, geometry, roof layers, plaques, ornaments, colors, lighting, and proportions.
- Image 2 is a strict frontend-rendered composition and typography layout plate. It defines the poster crop, six-column grid relationships, text bounding boxes, shared alignments, exact wording, type hierarchy, negative-space allocation, functional rule, and the intended overlap between text and architecture. Do not copy Image 2 as a flat screenshot; redraw the whole poster as one coherent printed design while following its layout very closely.

Primary request:
Transform Image 1 into a refined printed editorial poster, using Image 2 as the dominant spatial control. Keep the large architectural mass on the right and lower side, the open sky on the upper-left, and the strong rising diagonal formed by the repeated eaves. Keep the same approximate positions, sizes, line breaks, shared left edges, vertical axes, and rule endpoints shown in Image 2. The model may naturally redraw the letters, but the grid and typographic rhythm should remain visibly disciplined.

Typography and text, exactly as shown:
- top line: "DATONG ANCIENT CITY · 01"
- giant low-contrast background word on two lines: "TAIPING" then "LOU"
- large vertical Chinese title: "太平楼"
- small vertical place label: "大同古城"
No other text.

Typography roles:
- "太平楼": high-contrast modern Song/Ming display face, large vertical vermilion title, first-column anchored.
- "TAIPING / LOU": ultra-heavy geometric sans, pale blue-gray at low contrast, clipped to the sky region and visually behind the building.
- "大同古城": compact heavy sans, dark blue-black, aligned beside the main title.
- top line: small widely tracked bold sans, dark blue-black, connected to one precise horizontal rule.
Preserve the relative letter spacing and exact shared alignments from Image 2. Do not invent extra labels, metadata, stamps, seals, QR codes, microtext, or decorative English.

Architecture treatment:
Preserve the exact real building from Image 1. Keep the three repeated eave layers, top triangular gable, roof animals, colorful dougong, both real plaques, red lanterns, red facade, and the original low-angle diagonal perspective. Do not alter plaque text or add architectural elements.
Use restrained color separation: pale mineral blue paper-like sky; authentic vermilion and warm red architecture; deep blue-black roof shadows; muted gold and green structural details. Add fine offset-print halftone mainly in dark roof and wall areas, subtle warm-cream linework only on selected ridge/eave edges, and low-frequency paper fibers in the sky. Keep flat title color and smoother background type so architecture, text, and paper have different material frequencies.

Layer stack back-to-front:
pale fibrous sky -> low-contrast TAIPING/LOU structural type -> real stylized building -> vermilion 太平楼 and compact 大同古城 label -> top information line and functional rule.
The main Chinese title may touch or slightly overlap a low-information outer eave edge, but must not cover the roof animals, top gable, plaques, lanterns, or important dougong.

Constraints:
Preserve Image 1's photographed identity and exact perspective. Follow Image 2's layout substantially more closely than a text-only prompt. Keep a 3:4 portrait composition. Redraw everything cohesively; do not paste sharp digital text on top of a differently textured image. No post-compositing look, no extra objects, no people, no sun disc, no generic Chinese motifs, no logo, no watermark.

Avoid:
top-title/bottom-photo split; centered safe template; drifting text blocks; inconsistent left edges; random grid lines; uniform noise over all layers; invented architecture; fantasy reconstruction; extra copy; repeated titles.
```
