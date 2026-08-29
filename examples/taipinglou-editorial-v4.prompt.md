# 太平楼编辑排版整体重绘 V4

本次使用内置 `imagegen` 的 `style-transfer` 编辑流程。Image 1 是原照片，Image 2 是 [taipinglou-editorial-guide-v4.png](taipinglou-editorial-guide-v4.png)。垫图不含原照片像素，成品没有生成后的文字回叠。

```text
Use case: style-transfer.
Asset type: typography-first 3:4 vertical editorial travel poster about Chinese architecture.

Input roles:
- Image 1 is the edit target and sole source of Taiping Tower's real viewpoint, roof geometry, three eave levels, gable, roof animals, dougong, plaques, lanterns, windows, colors and identity.
- Image 2 is a frontend-rendered layout-only composition guide. It contains no target-photo pixels. Use it strictly for the six-column typographic field, exact text zones, type scale contrast, negative space, thin leader routes, architectural footprint and controlled occlusion. Its gray polygons are not a style or material reference.

Design priority:
Typography and architecture must form one poster composition. This is not a webpage, dashboard, museum kiosk, app or infographic. Do not create cards, label boxes, drop shadows, buttons, pills, badges, floating panels, repeated components or UI containers. All annotations remain unboxed bare typography. Hierarchy comes from type scale, weight, column alignment, whitespace, color reversal and one building/type occlusion.

Composition:
- Preserve Image 2's huge vertical vermilion "太平楼" on the left, giant pale "TAIPING" with smaller widely tracked "TOWER" behind the architecture, compact place/history typography in column 2, and unboxed feature annotations.
- The real diagonal building occupies the right and lower field and bleeds off the right and bottom edges.
- The building sits in front of the right side of pale TAIPING/TOWER and may trim only the right edge of the last Chinese character "楼" by about 5–8%. Do not overlap text with text.
- Keep the strong quiet negative space in the upper-left sky. Do not fill it with symbols or decoration.
- Follow the exact column starts and relative bounding boxes from Image 2; do not recenter the page and do not turn annotations into equal modules.

Architecture transformation:
- Strongly translate Image 1 into a four-color risograph/screenprint, not a raw photographic cutout.
- Quantize the building into three main tonal bands.
- Roof tiles, under-eave cavities and deep dougong shadows: deep indigo-black 45-degree halftone with visible ink dropout.
- Gable, walls, columns, windows, railings and lanterns: broad flat vermilion and brick-red planes with slight registration offset; remove glossy photographic gradients.
- Gold/green/blue painted details: restrained warm-cream, ochre and dark-olive spot colors.
- Important ridges, roof animals, eave tips, selected dougong edges and plaque frames: selective warm-cream engraved linework only.
- Add one subtle deep-indigo offset roof-silhouette echo up-left. No full-image edge detection.
- Preserve real plaque locations and architecture. Do not invent or rewrite plaque calligraphy.

Background:
Completely replace the photographic sky with pale mineral cyan/cold gray fibrous paper around #D8E3DF. Use low-frequency fibers, uneven roller wash and faint toner clouds. No natural lens gradient or clouds. Pale structural type remains smoother than the building halftone.

Typography and exact copy, no additional text:
"DATONG · SHANXI / EAST LANDMARK / 01"
"和阳街 × 太平街"
"TAIPING"
"TOWER"
"太平楼"
"大同古城 · 东部标志性节点"
"DATONG ANCIENT CITY"
"太平楼始建于明代，现存建筑为当代复建。"
"01 / 构件"
"斗拱"
"DOUGONG · 托起外檐"
"02 / 屋顶形制"
"十字歇山顶"
"CROSS XIESHAN ROOF"
"03 / 楼阁节奏"
"三层三檐"
"THREE EAVE LEVELS"
"照片可见匾额 / INSCRIPTION"
"四海升平"
"明代始建 · 当代复建"
"视觉观察与公开资料交叉核对"
"03 / 03"

Type roles:
- "太平楼": very large high-contrast Song/Ming-style vertical display type, vermilion, main focal point.
- "TAIPING / TOWER": oversized low-contrast geometric sans structural type behind the building.
- Place and history: compact neutral sans plus a short Song-style sentence, dark ink on sky, with one short vermilion rule above the sentence.
- Feature names: expressive Song/Ming display at medium scale; supporting indices and English are small sans.
- "十字歇山顶" is dark ink in the sky; "斗拱", "三层三檐" and plaque observation are warm-cream reversed bare type directly on dark architecture, with no background rectangle.
- "03 / 03" is a low-contrast editorial folio integrated into the lower-right architecture, not a badge.

Line and overlap contract:
- Thin leaders are 1–2px editorial hairlines, never thick connectors.
- Roof-form leader starts after the label, bends in clear sky, and touches the real upper roof-ridge boundary.
- Dougong leader lands on a visible dougong cluster.
- Three-eave leader lands on a repeated eave edge.
- No rule or leader crosses any glyph, plaque, roof animal or main ridge.
- No text-on-text collision. No decorative line without a routing or grouping function.

Constraints:
Preserve the real low-angle viewpoint, roof count/order, gable shape, ridge animals, dougong rhythm and plaques. No added architecture, people, sun disc, clouds, red circle, warrior, generic Chinese motifs, seal, QR code, logo or watermark. Do not misrepresent the reconstruction as an untouched Ming original.

Avoid:
website UI; information cards; beige boxes; shadows behind labels; button-like dates; pills; dashboard modules; equal repeated annotation components; raw photo cutout; simple color grade; continuous photo gradients; one uniform grain; random overlap; line through text; floating callout endpoint; extra microtext; visible grid; fantasy reconstruction.
```
