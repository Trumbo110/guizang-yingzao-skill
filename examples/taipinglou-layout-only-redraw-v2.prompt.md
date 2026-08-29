# 太平楼纯排版垫图整体重绘 v2

本次使用内置 `imagegen` 的 `style-transfer` 编辑流程。Image 1 是原照片，Image 2 是 [taipinglou-layout-only-guide-v1.png](taipinglou-layout-only-guide-v1.png)；垫图不含任何原照片像素，也没有进行生成后的文字回叠。

```text
Use case: style-transfer.
Asset type: 3:4 vertical contemporary Chinese architecture editorial travel poster.

Input roles:
- Image 1 is the edit target and the only source for Taiping Tower's real architecture, viewpoint, roof geometry, number and order of eave layers, gable, roof animals, dougong, plaques, lanterns, openings, proportions, and identity.
- Image 2 is a layout-only frontend plate. It contains no target-photo pixels and is NOT a visual-style or material reference. Its gray polygons only define the approximate building footprint and three rising eave diagonals. Its typography defines exact copy, bounding boxes, shared alignments, line breaks, scale hierarchy, negative-space allocation, and rule endpoints. Replace the gray placeholders with the strongly processed architecture from Image 1.

Primary request:
Create a visibly art-directed print poster, not a lightly filtered photograph and not a raw photographic cutout. Preserve Image 1's real architectural geometry while radically translating its surface into a three-to-four-color screenprint / editorial print language. Follow Image 2 closely for all typography and spatial layout.

Architecture extraction and transformation:
- Extract the complete right-and-lower architectural mass from Image 1, preserving all three repeated eave layers and the strong lower-left-to-upper-right rhythm.
- Inside the extracted architecture, compress tonal information into 3 main value bands rather than retaining continuous photographic gradients.
- Convert roof tiles, deep dougong shadows, recesses, and under-eave areas into deep indigo-black with clearly visible coarse 45-degree halftone dots and occasional ink dropout.
- Convert red walls, columns, windows, railings, lanterns, and the gable into broad flat vermilion and brick-red screenprinted planes with slight imperfect edge registration; do not keep glossy photographic gradients.
- Reduce gold, green, and blue painted details into small muted cream, olive, and ochre spot-color accents, only where they help identify the real structure.
- Add selective warm-cream engraved linework only along the most important roof ridges, eave tips, gable profile, and several major dougong edges. Do not outline every tile or turn the whole image into edge detection.
- Add a subtle deep-indigo offset shadow echo of the roof silhouette behind the building, displaced slightly up-left, to create a second printed layer and shallow spatial depth.
- Give the cutout a restrained warm-cream keyline only at major sky/roof boundaries. The architecture must look materially transformed and printed, not pasted from the original photo.

Sky and background transformation:
- Remove the original photographic sky completely.
- Replace it with a designed pale mineral-cyan and cold-gray paper field, approximately #CBDCDD to #DCE6E4, with low-frequency paper fibers, faint roller streaks, slight toner clouding, and a very subtle uneven screenprint wash.
- Keep the sky mostly flat and quiet enough for typography, but visibly more designed than the original sky. No photographic clouds, no natural lens gradient, and no blank white background.
- Structural background type should be smooth and low contrast so it is clearly a different material from the high-frequency halftone building.

Typography and layout from Image 2:
- top line exactly: "DATONG ANCIENT CITY · 01"
- giant low-contrast two-line structural type: "TAIPING" then "LOU"
- large vertical Chinese title exactly: "太平楼"
- small vertical place label exactly: "大同古城"
- no other text
Keep the frontend plate's shared first-column left edge, relative text block sizes, line breaks, vertical axes, horizontal rule start/end, red endpoint dot, and the controlled contact between the Chinese title and the outer eave. Render the title in a high-contrast modern Song/Ming face, vermilion. Render structural Latin in an ultra-heavy geometric sans, pale blue-gray. Render metadata and place label in compact dark indigo sans.

Layer stack:
mineral-cyan fibrous paper -> low-contrast TAIPING/LOU -> offset indigo roof-shadow echo -> transformed halftone/flat-color architecture -> vermilion 太平楼 and dark 大同古城 -> top metadata and functional rule.

Identity protection:
Do not change the camera angle, add or remove floors, alter the number/order of roofs, invent roof animals, redraw the gable into another shape, or cover the original plaques, main roof animals, lanterns, or key dougong with typography. Plaques remain part of the real architecture and must not be replaced by invented signage.

Constraints:
The output must show unmistakable posterization, color separation, halftone, selective engraving, paper texture, and slight registration error at normal viewing size. Image 2 controls layout only; do not inherit its gray placeholder colors. Redraw the whole poster cohesively. No post-overlaid digital text look, no extra objects, no people, no sun disc, no generic motifs, no logo, no watermark.

Avoid:
unchanged photo pasted onto a new background; raw photographic cutout; simple saturation boost; one uniform grain layer; photographic sky; soft cinematic color grade; full-image edge detection; overly detailed realism; extra copy; repeated title; decorative visible column grid; fantasy reconstruction.
```
