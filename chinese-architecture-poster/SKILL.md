---
name: chinese-architecture-poster
description: Transform user-shot photos of Chinese historic, vernacular, reconstructed, or Chinese-inspired architecture into truthful editorial travel posters and optional original/poster comparison collages. Use for architectural photo stylization, cultural travel covers, heritage-inspired layouts, or before-and-after assemblies; do not use for generic photo retouching or inventing buildings from scratch.
---

# Chinese Architecture Poster

把用户拍摄的真实建筑作为不可替换的主体，通过信息提纯、印刷化处理和编辑排版生成旅行海报。风格化不能改变建筑身份，也不能把当代仿古、修复或新建项目误写成历史遗存。

## 先判断任务

- 将用户照片标记为 **edit target**；其他样图只能作为风格参考，不能把其中的建筑、文字、标志或文化符号移入目标照片。
- 判断对象属于历史建筑、传统民居、历史街区、修复/重建项目，还是中国风当代建筑。仅凭外观不能断言年代或文保身份。
- 用户明确指定风格时遵从；未指定时按建筑语境选择：
  - 历史建筑或文保对象：`museum-print`。
  - 结构、营造或测绘感强：`survey-overlay`。
  - 当代院落、酒店、更新项目或街区：`editorial-grid`。
  - 社交媒体封面、强调冲击力：`screenprint-pop`。
  - 蓝紫夜游风只在用户明确要求或对象具有夜生活/商业语境时使用。
- 选择风格或构造提示词前，读取 [references/visual-style-analysis.md](references/visual-style-analysis.md)。

## 建立事实边界

- 海报上可以直接使用用户确认的建筑名和地点。
- 涉及年代、朝代、设计者、历史事件、文保级别或建筑功能时，先查可靠来源；优先项目官网、政府/文旅部门、文保机构和建筑事务所资料。
- 找不到可靠信息时只写已确认的名称、地点和中性描述，不补写“始建于”“千年古建”等猜测。
- 对当代中国风项目使用“当代院落”“城市更新”“传统语汇”等准确措辞，不制造古迹感。

## 提炼建筑

按四层信息处理，而不是对整张照片统一套滤镜：

1. **轮廓层**：保留屋顶坡度、飞檐、塔刹、层数、中轴和体量关系。
2. **结构层**：选择性保留斗拱、檐口、栏杆、门窗、牌匾、砖石和院落轴线。
3. **明度层**：压缩为 2–4 个主要明度，可采用黑白、单色或双色套印。
4. **质感层**：最后增加纸张、网点、抖动、漏印或颗粒；噪点不能遮蔽关键结构。

先做适度透视和构图校正，再分离主体、压低干扰背景。只在关键结构处描边；树叶、电线、游客和随机纹理不应获得与建筑同等权重。

## 生成海报

默认使用图像编辑而非重新生成场景。把建筑几何、相机视角、真实材料、光影逻辑和可辨识细节写成不变量，并明确：不得增加楼层、塔刹、脊兽、匾额、门窗或不存在的装饰。

版式遵循以下约束：

- 默认保持原图方向；旅行竖版优先 3:4，横版优先 4:3 或 16:9，除非用户指定平台比例。
- 使用 4 栏或 6 栏网格，复杂多图版可用 12 栏；外边距约为画布宽度的 5%–8%。
- 建立地点/建筑名、说明、副资料三级层级；最多两套正式字体和一套仅作点缀的书写体。
- 文字可以与建筑重叠，但避开塔刹、屋脊、牌匾、入口和决定身份的构件。
- 英文只能承载真实信息，不能用无意义字母制造“设计感”。
- 默认采用两个中性色加一个强调色，强调色主要用于标题、圆形、印章或分割线。
- 图片内只放必要短文案。要求逐字准确；若图像模型不能稳定渲染中文，先生成无字视觉底图，再用确定性排版工具叠字。

推荐的共享提示词结构：

```text
Use case: style-transfer
Asset type: editorial travel poster
Input images: Image 1: edit target and sole source of architectural geometry
Primary request: transform the real photo into <mode> while preserving the photographed building
Subject: <confirmed building and location>
Style/medium: high-contrast editorial print, selective linework, restrained print texture
Composition/framing: <grid, crop, title zone, negative space>
Color palette: <two neutrals plus one accent>
Text (verbatim): "<short confirmed title/location>"
Constraints: preserve geometry, viewpoint, proportions, rooflines, materials, and distinctive details; no invented architectural elements; exact text only; no logo; no watermark
Avoid: fake antiquity, fantasy reconstruction, generic Japanese motifs, illegible microtext, decorative clutter
```

## 验收

逐项检查：

- 建筑仍可由原照片直接辨认，层数、屋面、开口和中轴未被重构。
- 历史与地点文案均有依据；当代项目没有被误称为古建。
- 中文标题逐字正确，没有多余英文、伪二维码、品牌标识或水印。
- 颗粒、网点和描边服务于结构，不把树木或背景噪声变成主体。
- 标题和建筑主轮廓在缩略图尺寸下仍清晰，正文不过度细小。

若第一次结果仅有局部问题，每轮只修一个变量并重复建筑不变量，避免重写整套提示词造成主体漂移。

## 生成后询问拼图

海报交付后询问用户是否需要原图对照拼图；不要因为这是 skill 的能力就自动生成。

用户确认后使用 `scripts/make_comparison.py`：

- 原图为竖图时默认左右拼，原图在左、海报在右。
- 原图为横图时默认上下拼，原图在上、海报在下。
- 默认保留两张图的完整内容，允许成品比例随之改变；若用户要求固定平台比例，再询问是否允许裁切。

```bash
python3 scripts/make_comparison.py ORIGINAL POSTER OUTPUT
```
