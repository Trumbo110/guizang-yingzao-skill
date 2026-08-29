# 既下山·大同 v2 最终提示词规范

完整的空间设计见 [jixiashan-datong-blueprint-v2.md](jixiashan-datong-blueprint-v2.md)。本次使用内置 `imagegen` 的 `style-transfer` 编辑流程。

## 输入角色

1. `1787979917028.jpg`：唯一 edit target，也是建筑几何的唯一来源。
2. `b8465deed37cf34f45e0c578c8db79de.jpg`：只参考跨栏编辑秩序和橙灰文字系统。
3. `e0818d5582ed6b102db15d4a40ecb2f7.jpg`：只参考实景与对齐线稿的材质切换。
4. `02c45ca2c9a17665338811ecdae0e064.jpg`：只参考背景大字、建筑中景和红色前景字的层级。
5. `3e490d5baebc2c279f6854c209a525b9.jpg`：只参考粗网点建筑与细规则线的冲突。

风格参考中的建筑、文案、符号、品牌和文化图形不得进入结果。

## 最终提示词

```text
Create a dense but controlled 1024x1536 contemporary Chinese architecture editorial poster. Do not use a top-title/bottom-photo template. Typography, extracted architecture, color field, linework, and print materials must occupy one interlocked space. The hotel is a contemporary courtyard completed in 2025, not an ancient monument.

Use a strict 6-column grid with 5.5% margins, 1.6% gutters, and a 24px-like baseline. Align the courtyard and reflecting-pool centerline to the central gutter. About 75% of elements obey the grid. The only controlled breaks are the outer roof eaves bleeding beyond the outer columns and the main Chinese title crossing from columns 1–4 slightly into column 5.

The irregular cutout architecture fills the full width from about 16% canvas height through the bottom, so the roof and tree edge intrudes into the typography area; there is no rectangular photo boundary. Huge "DATONG" spans columns 1–6 at 3%–34% height. A smooth brick-red field spans columns 5–6 and bleeds right at 10%–47% height, behind the right roof. "既下山" spans columns 1–4 at 10%–24% height and crosses the architectural edge. Vertical "大同" sits in column 6 at 22%–41%. Vertical "东南邑" sits in column 1 at 43%–60% on a warm-white strip over a quiet dark wall. "SUNYATA DATONG" and "GOA / 2025" form a compact aligned metadata block in columns 1–2 at 69%–78% height.

Back-to-front layer stack: warm fibrous paper; giant low-contrast sand-gray "DATONG"; smooth brick-red field and a few functional rules; precisely aligned warm-white linework on only the left 35% of roof edges, wall edges, courtyard axis, and pool boundary; the real architecture as a cool blue-black and gray-blue duotone halftone cutout; foreground Chinese title and factual labels; a few thin rules connecting labels and pool boundaries, interrupted by architecture.

The real tree crowns, left roof, and central gate mask 20%–30% of "DATONG". The lower 6%–10% of "既下山" is locally hidden by real roof/tree edges without harming reading. Vertical brick-red "大同" is in front of the red field but behind the real right eave for about 10% of its strokes. The warm-white "东南邑" label overlaps a quiet left wall by about 20%. Do not cover distinctive roof slopes, the gate opening, curved passages, paired stone figures, pool edge, or courtyard centerline.

Typography roles: "既下山" uses one high-contrast modern Song/Ming display face; "DATONG" is an ultra-large condensed serif or grotesk at 15%–22% contrast and acts as a background shape; "大同" uses a vertical narrow heavy Chinese face in brick red; "东南邑" uses a vertical narrow neutral sans; metadata uses a small widely tracked neutral sans. These are functional roles, not competing decorative fonts.

Material map: low-frequency paper fibers in the background; coarse offset halftone on the right roof and walls; finer halftone on the central gate; precise warm-white linework only on the left 35%, never on leaves or random brick joints; a smooth deep blue-black pool retaining its real reflection; a flat smooth brick-red field. Never apply one uniform noise layer across everything.

Palette: paper #E9E5DA; architecture shadow #172027; architecture midtone #66717A; brick red #B8402E; ghost type #B99C75; pool #173447; linework #F1ECE1. Brick red must connect the field, vertical "大同", a small amount of contour, and the year/rule system.

Render exactly and only: "既下山", "大同", "东南邑", "DATONG", "SUNYATA DATONG", "GOA / 2025".

Preserve the target photograph's exact viewpoint, bilateral geometry, roof slopes, tile edges, central gate, curved passages, paired stone figures, walls, trees, pool, reflection, openings, proportions, and lighting logic. Do not add, remove, reconstruct, fantasy-restyle, or relocate architecture. No invented plaque, ornament, lantern, dragon, cloud, seal, QR code, microtext, logo, watermark, copied style-reference imagery, blank title band, centered safe magazine template, uniform monochrome material, or decorative grid without alignment function.
```
