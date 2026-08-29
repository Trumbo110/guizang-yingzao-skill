# 应县木塔：主题文字木刻海报提示词

本次使用内置 `imagegen` 的 `style-transfer` 编辑流程。图 1 是用户照片，图 2 是不含原图像素的排版垫图；没有在生成结果上重新叠字。

```text
Use case: style-transfer
Asset type: 3:4 vertical editorial cultural-travel poster

INPUT ROLES
- Image 1 is the edit target and the sole source of the real Yingxian Wooden Pagoda's architecture, camera viewpoint, plaques, trees, and geometry.
- Image 2 is a frontend-rendered layout-only reference. It contains no target-photo pixels. Follow its typography bounding boxes, six-column alignments, scale hierarchy, negative-space allocation, subject footprint, and occlusion direction. Replace its crude tower placeholder with the exact real tower from Image 1.

PRIMARY REQUEST
Transform Image 1 into a typography-first contemporary Chinese editorial poster. Preserve the strict low-angle central monument composition and the photographed pagoda's identity, while translating the whole image into a coherent limited-color woodblock / risograph print. Typography is the primary composition system; facts are thematic text, not educational callouts.

ARCHITECTURE INVARIANTS
- Preserve the exact photographed tower: its visible five exterior storeys and six eaves, roof slopes, stacked proportions, central axis, bracket-set rhythm, balconies, openings, existing plaque positions, and low-angle perspective.
- Do not add or remove storeys, eaves, finials, windows, balconies, plaques, dougong, or decorative structures.
- Keep the tower filling almost the entire frame, with its upper roof close to the top and the lower body naturally obscured by the original foreground trees.
- Keep the existing plaques as part of the architecture: preserve their placement and overall ink-calligraphy character; do not invent additional plaques or turn them into new poster labels.
- Keep the trees as foreground depth. Do not erase them to create an isolated product cutout.

REGIONAL MATERIAL TRANSFORMATION
- Sky/background: replace the smooth photographic blue with mineral pale celadon-blue paper, low-frequency fibers, faint roller variation, and subtle aged offset-print grain.
- Pagoda: compress into four tonal inks—near-black umber, dark walnut, warm copper/ochre, and paper cream. Use dense high-frequency halftone and selective wood-engraving-like linework on roof tiles, eave undersides, bracket sets, railings, and timber joints. Walls and broad timber planes use calmer middle-frequency flat color. Preserve warm wood identity, but remove continuous photographic gradients.
- Trees/foreground: change the bright green foliage into deep pine green and blue-black coarse halftone masses. Preserve recognizable occlusion contours, but simplify tiny leaf noise so the trees remain a foreground plane rather than competing with the tower.
- Add only restrained cyan/Prussian-blue misregistration at a few outer edges; never distort the true silhouette.
- The sky, tower, and trees must visibly use different texture frequencies. Do not apply one uniform noise layer.

COLOR
Mineral celadon-blue paper; near-black brown; warm walnut and ochre; deep pine green; vermilion accent. Vermilion should connect the main Chinese title with only a very small amount of supporting copy, not become a generic red sun or seal.

TYPOGRAPHY AND GRID
Follow Image 2 closely.
- Large muted ochre “1056” at the upper left, spanning the first four columns, behind the top roof. The roof should occlude about 20–30% of the numerals.
- Small black “辽 · 清宁二年” below the year, aligned to the same left edge.
- Large low-contrast narrow sans “YINGXIAN” and smaller “WOODEN PAGODA” across the middle sky behind the pagoda. The tower may hide 25–45%, but recognizable fragments must remain on both sides.
- Huge vertical vermilion “应县木塔” down the left edge in a high-contrast Song/Ming-style display face. It may overlap only the low-information outer eave edges and tree shadow by about 5–10%; protect the central plaques, main roof ridges, finial, and key bracket sets.
- Small “山西 · 朔州 · 应县” at upper right, aligned to the right margin.
- Vertical warm-cream “佛宫寺释迦塔” along the right dark zone.
- Bottom warm-cream theme cluster: “五层六檐　纯木楼阁”, with small “FIVE STOREYS · SIX EAVES” directly beneath it.
- Use sharp shared left edges, right edges, baselines, and deliberate spacing. Allow small natural glyph drift, but preserve the layout hierarchy and alignment groups.

EXACT ADDED COPY — use only these strings and no other added text:
“1056”
“辽 · 清宁二年”
“应县木塔”
“YINGXIAN”
“WOODEN PAGODA”
“山西 · 朔州 · 应县”
“佛宫寺释迦塔”
“五层六檐　纯木楼阁”
“FIVE STOREYS · SIX EAVES”

LAYER STACK
Celadon paper -> low-contrast year and Latin structure type -> exact stylized pagoda -> deep-green foreground trees -> vermilion main title and cream supporting type.

HARD NEGATIVES
- No visible line primitives: no grid lines, leader lines, rules, dividers, borders, underlines, arrows, callout endpoints, diagrams, or annotation paths.
- No educational labels, component definitions, numbered callouts, paragraphs, or dense microtext.
- No cards, pills, buttons, badges, UI panels, rounded boxes, repeated label components, or drop shadows.
- No red sun, seal, 祥云, dragon, Buddha illustration, people, maps, diagrams, QR code, logo, page number, random symbols, watermarks, or orphan corner decoration.
- No top-text/bottom-photo split.
- No raw photographic cutout pasted onto a new background; the tower, sky, and trees all require the described region-specific print treatment.
- No fantasy reconstruction, no architectural additions, no extra words or fake Latin.
- Output one finished full-bleed poster artwork, no mockup and no outside margin.
```
