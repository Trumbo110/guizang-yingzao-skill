# 大同圣母圣心堂 V2：氧化朱砂背景修订提示词

本轮是单变量修订：保持 V1 已成立的双塔比例、网格、文案与遮挡关系，只替换综合色相和区域配色。图 1 是原始照片，图 2 是氧化朱砂配色的 `layout-only` 垫图。

```text
Use case: style-transfer
Asset type: 3:4 vertical editorial cultural-travel poster, V2 palette revision

INPUT ROLES
- Image 1 is the edit target and sole source of the real Datong Sacred Heart Cathedral towers, camera viewpoint, arches, domes, crosses, brickwork, trees, lighting direction, and geometry.
- Image 2 is a frontend-rendered layout-only palette and composition reference. Follow its six-column typography layout, exact text placements, subject footprints, occlusion direction, and oxide-red / terracotta background palette. Replace its crude tower placeholders with the exact photographed architecture from Image 1.

SINGLE TARGETED REVISION
The previous concept stayed too close to the original black night sky. Replace every former sky / negative-space area with an opaque matte oxidized vermilion / terracotta paper field, approximately burnt cinnabar #B75B3F, with subtle lighter clay roller variation. Leave no photographic black sky, navy sky, dark vignette, black gradient, or nighttime background tone around the towers. This is a graphic color field, not a tinted night photograph.

PRESERVE
- Preserve the taller left/front tower and shorter right/rear tower, their unequal dimensions, viewpoint, arches, panels, brickwork, domed caps, crosses, scaffolding, crop, and lower-tree occlusion.
- Preserve the V1 six-column positions and controlled occlusions for `1906`, the stepped Latin structure words, vertical Chinese title, and bottom theme cluster.
- Do not mirror, equalize, simplify, or reconstruct the towers; do not reveal an unseen façade or add architecture.

NEW COLOR SEPARATION
- Former sky: opaque oxidized vermilion / terracotta paper, low-frequency fibers and restrained dot grain.
- `1906` and vertical Chinese title: deep petroleum green-black.
- Latin structure type: transparent brick-red and petroleum-gray.
- Towers: warm bone-white / parchment wall planes, cool celadon / petroleum shadow ink, deep green-black arch interiors; high-frequency linocut and screenprint treatment throughout.
- Crosses: controlled warm-ivory print bloom, not neon.
- Trees: deep pine-green / near-black coarse halftone with selective ochre underprint. Dark foreground must not creep upward into the terracotta sky.
- Bottom readable text: parchment cream; small English theme line: warm peach / ochre.

TEXT — exact strings only
“1906”
“重建 · REBUILT”
“山西 · 大同 · 都司街”
“SACRED”
“HEART”
“CATHEDRAL”
“圣母圣心堂”
“大同古城”
“双钟楼　拱券　古城夜色”
“TWIN BELL TOWERS · ARCHES · NIGHT”
“DATONG · DUSI STREET NO. 4”

HARD NEGATIVES
No black or navy sky, dark background, vignette, gradient to black, visible grid, rules, dividers, borders, leader lines, annotations, cards, UI, added religious icons, extra crosses, statues, people, maps, seals, QR codes, logos, watermarks, orphan decorations, fantasy architecture, raw photographic cutout, extra words, or fake Latin. Output one full-bleed finished poster.
```
