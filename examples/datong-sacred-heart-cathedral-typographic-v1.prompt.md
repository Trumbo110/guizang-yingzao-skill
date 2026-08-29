# 大同圣母圣心堂：双塔夜色主题文字海报提示词

本次使用内置 `imagegen` 的 `style-transfer` 编辑流程。图 1 是用户照片，图 2 是不含原图像素的排版垫图；没有在生成结果上重新叠字。

```text
Use case: style-transfer
Asset type: 3:4 vertical editorial cultural-travel poster

INPUT ROLES
- Image 1 is the edit target and the sole source of the real Datong Sacred Heart Cathedral towers, camera viewpoint, arches, domes, crosses, brickwork, trees, lighting direction, and geometry.
- Image 2 is a frontend-rendered layout-only reference. It contains no target-photo pixels. Follow its typography bounding boxes, six-column alignments, type scale hierarchy, negative-space allocation, subject footprint, and occlusion direction. Replace its crude geometric tower placeholders with the exact two photographed towers from Image 1.

PRIMARY REQUEST
Transform Image 1 into a typography-first contemporary Chinese editorial poster about 大同圣母圣心堂. Preserve the exact asymmetric double-tower night photograph, but materially reinterpret every region as a limited-color screenprint / linocut / offset-print artwork. Typography is the composition system; factual words are thematic atmosphere, not educational annotations.

ARCHITECTURE INVARIANTS
- Preserve the exact photographed pair: the taller left/front bell tower and the shorter right/rear bell tower, their unequal heights and widths, side-view perspective, arched openings, rectangular relief panels, cornices, pale brick masonry, domed caps, round finials, existing crosses, ladders/scaffolding visible in the source, and the amount of lower building hidden by trees.
- Keep both crosses exactly where they are and preserve their photographed shapes. Reduce the blown digital halo, but keep warm luminous bone-white light.
- Do not mirror the towers, make them equal, turn them into Gothic spires, expose an unseen central façade, add a nave, windows, statues, bells, plaques, decorative crosses, or any fantasy reconstruction.
- Keep the original crop and low-angle night viewpoint. The two towers must still be immediately recognizable as this specific photograph.
- Keep the original foreground trees and their occlusion. Do not erase them to create a product cutout.

REGION-SPECIFIC MATERIAL TRANSFORMATION
- Sky/background: replace flat photographic black with deep ink-blue / black-green dyed paper, low-frequency fibers, subtle indigo roller variation, tiny aged offset flecks, and restrained uneven ink density. No stars, moon, clouds, gradient glow, or empty digital black.
- Taller tower: compress into bone-white, pale celadon-gray, dark blue-green shadow, and warm amber light. Render brick courses, arch moldings, cornices, dentils, and relief panels with high-frequency linocut hatching plus fine screenprint dots. Broad wall planes use calmer middle-frequency flat ink. Add very restrained cyan and charcoal misregistration only at a few outer edges without changing the silhouette.
- Shorter tower: use the same palette but one step lower contrast and slightly coarser / calmer texture than the taller tower, preserving real depth and scale difference.
- Crosses and openings: warm bone-white and amber two-ink glow with a small soft print bloom; no neon effect. The interior of the arches remains deep black with localized amber spill.
- Trees/foreground: convert bright green leaves into deep pine green and near-black coarse halftone masses. Preserve the real tree contours and occlusion, simplify individual leaf noise, and keep the existing orange garden light as an irregular amber roller underprint. Do not paint detailed botanical illustrations.
- The sky, taller tower, shorter tower, and trees must visibly use different texture frequencies. Never apply one uniform noise filter across everything.

COLOR
Deep ink blue-black paper; bone-white stone; pale celadon gray; dark pine green; warm amber / muted ochre light. Amber connects the large year, vertical Chinese title, crosses, and only a small amount of supporting type. No bright red.

TYPOGRAPHY AND GRID — FOLLOW IMAGE 2 CLOSELY
- Six-column 3:4 grid, generous dark negative space, no visible grid lines.
- Large muted amber Bodoni-style “1906” bleeding from the upper left across the first five columns, behind the taller tower and its cross. The tower should occlude part of the 0 / 6 region, while enough of all four numerals remains recognizable.
- Small bone-white “重建 · REBUILT” below the year, aligned with the left margin.
- Small bone-white “山西 · 大同 · 都司街” at the upper right, aligned to the right margin.
- Large low-contrast narrow sans “SACRED”, indented “HEART”, and smaller high-contrast serif “CATHEDRAL” in three stepped rows behind the towers. The buildings may hide 25–45% of these structure words, but fragments should remain on both sides.
- Huge vertical muted-amber “圣母圣心堂” along the first column in a high-contrast Song/Ming-style display face, foreground layer. It may overlap only the left outer edge of the taller tower by about 5–8%. Protect both crosses, both domes, both arched openings, major cornice transitions, and the silhouette gap between towers.
- Bottom theme cluster on the dark tree mass, sharing one sharp left edge: large bone-white “大同古城”; smaller bone-white “双钟楼　拱券　古城夜色”; small amber “TWIN BELL TOWERS · ARCHES · NIGHT”. Give each row its own clean baseline and breathing room.
- Small bone-white “DATONG · DUSI STREET NO. 4” at lower right, aligned to the right margin.
- Use deliberate shared edges, baselines, and spacing. Small natural glyph drift is acceptable; preserve the layout hierarchy and alignment groups.

EXACT ADDED COPY — use only these strings and no other added text:
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

LAYER STACK
Ink-blue paper -> low-contrast year and Latin structure type -> exact stylized twin towers -> deep-green foreground trees with amber underprint -> vertical amber Chinese title and fully readable bottom theme text.

HARD NEGATIVES
- No visible line primitives: no grid lines, leader lines, rules, dividers, borders, underlines, arrows, callout endpoints, diagrams, or annotation paths.
- No educational labels, component definitions, numbered callouts, paragraphs, historical timeline, captions, or dense microtext.
- No cards, pills, buttons, badges, UI panels, rounded boxes, repeated label components, or webpage layout.
- No added cross icons, religious emblems, saints, statues, stained glass, doves, candles, people, maps, seals, QR code, logos, page numbers, random symbols, watermarks, red sun, or orphan corner decoration.
- No top-text / bottom-photo split.
- No raw photographic tower pasted onto a new background. Sky, each tower, crosses, openings, trees, and lights must receive the described region-specific print treatment.
- No fantasy reconstruction and no extra words or fake Latin.
- Output one finished full-bleed poster artwork, no mockup and no outside margin.
```
