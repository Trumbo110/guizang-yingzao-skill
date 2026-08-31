---
name: chinese-architecture-poster
description: Transform user-shot photos of Chinese historic, vernacular, reconstructed, or Chinese-inspired architecture into truthful editorial travel posters and optional original/poster comparison collages. Use for architectural photo stylization, cultural travel covers, heritage-inspired layouts, or before-and-after assemblies; do not use for generic photo retouching or inventing buildings from scratch.
---

# Chinese Architecture Poster

把用户拍摄的真实建筑作为不可替换的主体，通过信息提纯、印刷化处理和编辑排版生成旅行海报。风格化不能改变建筑身份，也不能把当代仿古、修复或新建项目误写成历史遗存。

## 决策优先级

按以下顺序解决问题；后一层不能破坏前一层：

1. **排版与空间关系**：网格、文字尺度、留白、建筑占位和遮挡先成立。
2. **建筑身份**：真实轮廓、层数、屋顶、视角和地点特征必须保留。
3. **图像转译**：建筑、天空、前景和环境分别获得可见的限色与材质处理。
4. **事实语境**：经核实的年代、地点、门名或构件词进入字体系统。
5. **装饰**：只有同时服务主题和构图时才保留；孤立、无来源或仅为填空的元素删除。

这是一张编辑海报，不是网页、导览牌或构件科普图。默认先把事实变成排版材料，再考虑是否需要解释。

## 生成前先确认三件事

在检索、选 Token、写蓝图或调用图像生成之前，先从用户消息中提取以下答案。已经明确给出的不重复追问；缺失项合并成一次简短提问，不分多轮询问。

1. **地点、背景与文案**：建筑/街区名称、城市或地址，用户知道的背景，以及必须出现或禁止出现的文案。若用户没有自备文案，再确认是“由 Skill 检索后提炼短词”，还是“只使用用户确认的名称与地点”。用户不知道建筑名时，可以回答“不知道，请协助识别”，不能据外观直接编造。
2. **生成数量**：本次需要几张独立海报方案。数字指不同构图/材质方案的张数，不把原图对照拼图计入海报张数。
3. **是否生成原图对照拼图**：在海报生成前确认。选择“是”时，竖向原图默认原图在左、海报在右；横向原图（包括 16:9）默认原图在上、海报在下。多张海报默认每张各生成一张对应拼图；正方形、混合方向或用户要求固定平台比例时再确认方向/裁切。

可一次性这样询问：

```text
生成前确认一下：
1. 这是哪里、有什么背景？有没有必须加入或不要出现的文案（也可以让我检索提炼）？
2. 这次要生成几张不同方案？
3. 要不要同时生成原图对照拼图？竖图默认左右拼，横图默认上下拼。
```

只有三项都有答案后才开始生成。用户回答“你决定”也算授权 Skill 选择；此时默认生成 1 张，文案采用已确认名称/地点与可核实短词，拼图默认不生成。

## 三阶段模板化工作流

模板不是固定画框，而是一组可以追溯来源、具有兼容条件的设计变量。不要先选择一个风格名再套效果。

### 1. 分析并抽离要素

- 将用户照片标记为 **edit target**；其他样图只能作为参考，不能把其中的建筑、文字、标志或文化符号直接移入目标照片。
- 用 `scripts/design_tokens.py query` 按照片标签、类别或兼容关系检索 [references/design-tokens.json](references/design-tokens.json)，并以稳定 ID 记录候选；不要为普通任务整份加载 JSON。需要新建 Token、调整 Recipe 或理解解析规则时才读 [references/token-system.md](references/token-system.md)。预览色片不是强制配色。
- 读取 [references/design-element-library.md](references/design-element-library.md)，逐项分析内容、字体角色、网格、建筑类型与占位、背景、颜色、图形、材质、遮挡和信息密度。
- 使用内置参考组时读取 [references/reference-encoding-matrix.md](references/reference-encoding-matrix.md)。新参考图也按相同字段编码；把“观察到什么”“为何有效”“可借用什么”“何时不适用”分开。
- 使用 `参考/参考新/` 扩展组时逐张读取 [references/reference-encoding-expansion-2026.md](references/reference-encoding-expansion-2026.md)。不得跳到末尾只抄归纳；纯文字图只提供字体/网格机制，外国建筑与纯外文图必须执行中式转译门。
- 先穷举候选要素，再删减。每个要素都要说明视觉任务；没有任务的装饰不进入候选集。
- 对外国参考先写“视觉机制、目标照片几何对应、中文语义接管、地域材料接管、跨文化删除项”。可以迁移字窗、尺度、分栏、遮挡和材质关系，不能迁移外国地名、建筑、宗教符号、人物、徽章、纹样、品牌和广告。

### 2. 推断建筑处理

- 判断对象属于历史建筑、传统民居、历史街区、修复/重建项目，还是中国风当代建筑。仅凭外观不能断言年代或文保身份。
- 分析目标照片的建筑类型、视角、主体占比、中轴/透视线、负空间、背景杂乱度、可辨识构件、原生颜色和可分材质区域。
- 先执行 `cap.subject.preflight-rectification`：判断相机滚转、梯形透视、建筑真实坡度和真实不对称；需要时先扶正中轴与主要水平参照，再重新居中和裁切，之后才允许抠图、材质化和入版。
- 校正后的图像是建筑提取底图。裁掉透视变换产生的空白楔形、被截断的边缘碎片、无叙事作用的现代杂物和过量空区；但不得为追求对称而拉平飞檐、复制构件或修改匾额。
- 依据这些条件决定抠整座建筑、屋顶线、立面、局部构件、街巷透视或多块碎片；不能因为某张参考图用了完整抠图就默认抠完整主体。
- 读取 [references/mixing-logic.md](references/mixing-logic.md)，为抠图范围、主材质、辅助材质、背景类型和特效写出因果理由。

### 3. 有逻辑地混搭

- 从候选集中选择一个基础构图、一个建筑提取策略、一个主材质、最多一个辅助材质、一套字体角色系统、一套颜色逻辑、一个主要空间冲突和可选的语境插入层。
- 记录所选 Token ID，递归展开 `requires`，检查 `conflicts` 和 `mutex_groups`。任何硬冲突、依赖缺失或槽位超额都必须更换 Token，不能靠透明度或减少面积假装兼容。
- 主体容器（字窗/连续竖窗/同轴多窗/模块拼贴）、背景尺度（来源正文场/重复短地名/尺度数字）和语境材料（地形场/区域纹样/可信档案）三类各最多选择一个；不要把扩展库变成元素清单全叠。
- 允许从不同参考图取要素，但每项都要记录来源机制、与当前照片的兼容理由，以及它与其他已选要素的关系。
- 混搭不是取平均。先建立一个主导机制，再用 1–2 个次要机制补足；不要让中心纪念碑、强对角线、密集拼贴等多个基础构图同时竞争。
- 填写 [references/composition-blueprint.md](references/composition-blueprint.md)，通过兼容性和失败检查后才能生成。

## 建立事实边界

- 用户给出建筑名、城市、街区或地址时，默认先读取 [references/research-and-annotation.md](references/research-and-annotation.md)，检索并建立事实卡；不要只把用户给的几个字重复排版。
- 海报上可以直接使用用户确认的建筑名和地点。地点检索要先消歧，再把完整地址压缩为路口、街区或城市节点标签。
- 涉及年代、朝代、设计者、历史事件、文保级别、现存状态或建筑功能时，先查可靠来源；优先项目官网、政府/文旅部门、文保机构、建筑事务所、地方志与正式出版物。
- 将内容分为 `VERIFIED`、`OBSERVED`、`USER-CONFIRMED`、`UNCONFIRMED`。只有前三类可进入海报；照片观察不能被写成历史结论。
- 对复建、迁建和修复项目同时写清“历史源流”与“现存状态”，不能让 `始建于明代` 被理解为现存木构就是明代原构。
- 找不到可靠信息时只写已确认的名称、地点和中性描述，不补写“始建于”“千年古建”等猜测。
- 对当代中国风项目使用“当代院落”“城市更新”“传统语汇”等准确措辞，不制造古迹感。
- 从事实卡选择 3–7 个信息单元：名称、地点、时间关系、形制/构件、可见题字或城市关系。信息数量服从版面，不为凑满而加字。
- 默认采用“主题文字模式”：把经核实的年代、门名、构件词和地点词作为字形、节奏、背景结构或反白文字，不解释“它是什么”，也不画指向线。只有用户明确要求建筑科普、构件解析或导览图时，才启用“解释注释模式”；此时构件标签必须指向照片中的真实对象，并为引线预留不穿字的路由。

## 提炼建筑

按四层信息处理，而不是对整张照片统一套滤镜：

1. **轮廓层**：保留屋顶坡度、飞檐、塔刹、层数、中轴和体量关系。
2. **结构层**：选择性保留斗拱、檐口、栏杆、门窗、牌匾、砖石和院落轴线。
3. **明度层**：压缩为 2–4 个主要明度，可采用黑白、单色或双色套印。
4. **质感层**：最后增加纸张、网点、抖动、漏印或颗粒；噪点不能遮蔽关键结构。

先做透视和构图预检，再分离主体、压低干扰背景。正立面与中轴构图默认把建筑主轴校正到垂直方向约 `±0.5°`；斜拍则保留有叙事意义的透视，但仍消除无意相机滚转。校正后重新裁切，不把空白角、半截路人、无意义树枝或现代边缘碎片带进海报。只在关键结构处描边；树叶、电线、游客和随机纹理不应获得与建筑同等权重。

## 先写构图蓝图，再生成海报

默认使用图像编辑而非重新生成场景。把建筑几何、相机视角、真实材料、光影逻辑和可辨识细节写成不变量，并明确：不得增加楼层、塔刹、脊兽、匾额、门窗或不存在的装饰。

在调用图像工具之前，先用 [references/composition-blueprint.md](references/composition-blueprint.md) 写出本次海报的：

1. 原图预检：建筑主轴、水平参照、相机滚转、梯形透视、裁切范围与不可变形区域。
2. 画布、栏数、边距、沟槽和基线。
3. 文案清单及每段文字的字体角色、尺度、跨栏和前后层级。
4. 建筑的抠图边界、保留特征及各区域的材质处理。
5. 从背景到前景的 z 轴层级表。
6. 文字与建筑的遮挡对象、方向、比例和不可遮挡区。
7. 背景、色块、建筑、线稿和水面之间的明度、色相与纹理差异。
8. 信息模式：默认填写主题词的字体角色、栏位和层级；只有“解释注释模式”才填写标签来源、目标构件、引线路由、终点和禁穿区。
9. 外来参考的中式转译：保留的机制、目标建筑对应物、必须删除的文化内容，以及至少两个来自目标建筑的独有锚点。
10. Recipe（若使用）、候选 Token、依赖展开结果、互斥/冲突检查及因本张照片产生的参数覆盖。

蓝图不能只写“六栏网格”“标题与建筑重叠”这类抽象要求，必须指出元素跨第几栏、在哪条轴线上相遇、谁遮住谁，以及遮挡多少。

版式遵循以下约束：

- 默认保持原图方向；旅行竖版优先 3:4，横版优先 4:3 或 16:9，除非用户指定平台比例。
- 使用 4 栏或 6 栏网格，复杂多图版可用 12 栏；外边距约为画布宽度的 5%–8%，沟槽约为 1.2%–2%。至少 70% 的元素服从网格，只允许 1–2 个有目的的破格点。
- 建立展示标题、结构性大字、地点标签、资料文字等不同角色。字体差异必须对应角色差异，不能只是换字体；最多两套正式字体和一套仅作点缀的书写体。
- 主标题必须在缩略图中承担第一层级：其可见笔画量默认至少为资料字的约 `2.5–4 倍`，不得用接近正文的细字重。建筑名被拆成地点词和对象词时，二者仍视为一个标题组，不能各自在画面中自由漂移。
- 跨字体或跨方向的标题组使用 `cap.primitive.optical-alignment`：除了 CSS/SVG 文本框，还要检查实际可见字面、首尾基线和边缘留白。一个组至少共享两个可解释的边界或基线；仅仅“看起来差不多在左上角”不算对齐。
- 采用三轨竖向标题时，按 `左：真实拼音微字 / 中：重字重对象名 / 右：较小地点限定词` 组织。三轨由同一组网格变量计算，至少共享一条顶边和一条底边或基线；中文对象名保持绝对主导。
- 至少建立三个可辨认的空间层：背景纸/结构字或色块、建筑主体、前景标题或资料标签。禁止默认采用“上半部纯文字、下半部完整矩形照片”的两段式模板。
- 至少设计两处受控遮挡：一处让建筑遮住低对比结构字，另一处让短标题或标签压在建筑上。避开塔刹、主屋脊、牌匾、入口和决定身份的构件。
- 建筑与背景不能共享同一种材质。纸张使用低频纤维，建筑使用高频网点/线刻/实景颗粒，几何色块保持相对平滑；水、玻璃等反光面可保留平滑照片质感作为材质对照。
- 英文只能承载真实信息，不能用无意义字母制造“设计感”。
- 分割线和注释引线不得穿过可读字形。除非蓝图明确定义了文字蒙版、前后层级和语义目的，否则任何穿字都判为排版失败。
- 用户要求“不画线”时，版式中不得出现分割线、规则线、边框、引线、下划线或用线模拟的装饰；层级完全依靠字级、字重、颜色、留白、栏位与遮挡建立。
- 每一处重叠必须写成“参与元素、共同轴线、z 顺序、重叠范围、视觉目的、保护区”的重叠契约；只有靠得很近或随机压住不算空间设计。
- 海报不是网页：默认禁止把构件注释做成一组重复的卡片、徽章、按钮、圆角容器或带投影的信息组件。资料应先成为同一字体场中的边栏、窄列、反白小字或无底色注释；只有局部对比无法解决时才允许一个无投影的扁平色条。
- 默认采用两个中性色加一个强调色；优先从建筑原生色、地域材料或拍摄光线中取色，并让强调色连接至少两类元素。不要默认添加红圆、印章、短线或其他“东方海报”符号。
- 使用外国参考的配色时只保留冷暖、明度和面积关系，具体颜色重新从目标建筑的朱墙、青瓦、灰砖、木色、琉璃、黄土、煤黑、石灰或现场光线取样；禁止保留原参考的国旗色、宗教色和品牌色。
- 字窗、连续竖窗和同轴多窗只是构图容器，不算图像风格化。窗内建筑仍须进行 2–4 阶明度压缩，并在网点、线刻、双色套印、区域平涂或局部原色中至少选择两项。
- 使用来源正文、诗文、题记、年份、层数、高度、长度、图纸、旧照或传统纹样时必须记录来源。无来源则删除；照片轮廓抽取不能冒充测绘图，随机数字不能冒充历史数据。
- 默认的“主题文字模式”不使用可见规则线、边框、引线、下划线、箭头或标注端点。网格只存在于设计和检查阶段；只有用户明确要求信息图、测绘感或构件解析时，功能线才可进入成图。
- 图片内只放必要短文案。默认不把未经程序验收的真实文字排版图交给图像模型；需要布局参考时先读取 [references/frontend-layout-guide.md](references/frontend-layout-guide.md)，使用无文字的几何骨架。只有完整文字排版通过字体加载、字面测量、碰撞、溢出和共享轴检查后，才允许作为模型输入。

## 排版垫图条件启用

前端排版不是必经步骤。不能证明垫图本身正确时，错误的视觉证据比纯提示词危害更大。默认采用以下顺序：

1. **纯提示词**：文字很少、对齐关系简单时直接生成，不制作垫图。
2. **`geometry-only` 骨架（默认参考模式）**：需要约束建筑占位、主轴、背景色场或负空间时，只提供无文字的主体剪影与区域边界；不画文字框、伪字、空卡片或可见网格。
3. **`typeset-guide` 完整文字垫图（门控模式）**：只有当本地流程能够加载确定字体、测量实际字面并自动检查全部文字块时才启用。手写 SVG 坐标、逐字手调 `x/y` 或凭肉眼判断的图禁止作为输入。
4. 完整文字垫图必须通过 `cap.policy.typeset-guide-gated`：字体无回退、文字块无碰撞、无画布溢出、禁穿区无侵入、标题组共享轴成立、竖排顺序正确。任一失败立即降级为 `geometry-only` 或纯提示词，不“差不多通过”。
5. `grid-check` 只供检查；模型只能接收关闭调试线的骨架或已通过门控的 `typeset-guide`。主题模式不得保留功能线、文字框、边界框或网格栏线。
6. 将原照片标为 Image 1 `edit target`；可选的 Image 2 只控制已验证的几何/排版关系，不提供建筑像素。垫图不能替代建筑区域材质、背景替换和身份保护方案。
7. 不在生成结果上默认重新堆叠文字。若图像模型仍破坏已验证的标题组，整体重绘或减少文字，不用后贴字掩盖失败。

无论选择哪种模式，提示词都要显式给出层级栈、跨栏区域和遮挡比例：

```text
Use case: style-transfer
Asset type: editorial travel poster
Input images: Image 1: edit target and sole source of architectural geometry; Image 2: optional frontend-rendered composition/layout reference
Primary request: transform the real photo into <mode> while preserving the photographed building
Subject: <confirmed building and location>
Output count: <confirmed number of independent poster variants>
Comparison collage: <no / one per poster; portrait side-by-side / landscape stacked>
Information mode: thematic typography by default / explanatory annotation only when explicitly requested
Grid: <columns, margins, gutters, baseline, subject spans, text spans, controlled break>
Alignment groups: <elements sharing each left edge, right edge, center axis, or baseline>
Selected modules: <one subject container or none; one background-scale mechanism or none; one context-material layer or none>
Design tokens: <resolved cap.* IDs; include no unresolved recipe aliases>
Layer stack back-to-front: <paper> -> <ghost type/shape> -> <architecture plate> -> <foreground title/labels>
Occlusion map: <element A hides B by x%; C sits over D; protected areas>
Typography roles: <display Chinese, structural Latin, metadata sans, exact spans and scale>
Typography source: <verified title, short facts, source text, pinyin/translation; no invented copy>
Material map: <paper grain, flat color plane, architecture halftone/linework, smooth reflective region>
Architecture transformation: <cutout scope, 2–4 value bands, region-by-region posterization, halftone, engraving, misregistration>
Background transformation: <replace/retain; color field, texture frequency, gradient or flatness; at least two deliberate differences from the original photo when strong stylization is requested>
Color separation: <background, subject ink, midtone, accent; boundary contrast>
Cross-cultural translation: <reference mechanism retained; Chinese semantics and local material source; foreign buildings, symbols, motifs, brands, ads, QR codes, people and filler text removed>
Line policy: none in thematic typography mode; otherwise list each functional line and its endpoints
Text (verbatim): "<confirmed copy only>"
Constraints: preserve geometry, viewpoint, proportions, rooflines, materials, and distinctive details; no invented architectural elements; exact text only; no logo; no watermark
Avoid: top-text/bottom-photo template, disconnected title zone, unchanged photographic cutout, uniform grain on every layer, visible grid lines in thematic mode, decorative lines, web UI cards, fake antiquity, illegible microtext, orphan decorations
```

## 验收

逐项检查：

- 建筑仍可由原照片直接辨认，层数、屋面、开口和中轴未被重构。
- 相机滚转已经在建筑入版前处理；正立面主轴基本垂直，主要水平参照不再无意倾斜。透视校正没有拉平真实屋坡、飞檐或建筑不对称，变换后的空白角和干扰碎片已被重新裁切。
- 历史与地点文案均有依据；当代项目没有被误称为古建。
- 中文标题逐字正确，没有多余英文、伪二维码、品牌标识或水印。
- 颗粒、网点和描边服务于结构，不把树木或背景噪声变成主体。
- 当蓝图要求强风格化时，建筑内部已经发生可见的限色、明度压缩和区域材质变化，天空/背景也按方案重建；若仍像原照片抠图加统一颗粒，判为未通过。
- 标题和建筑主轮廓在缩略图尺寸下仍清晰，正文不过度细小。
- 主标题比资料字明显更重；拆分的地点词、对象名和可选拼音属于一个可解释的对齐组，至少共享两个字面边界或基线。若三个部分只是分别摆在邻近区域，判为未通过。
- 能明确指出至少三个 z 轴层级、两种不同材质和两处受控遮挡；若文字与图片仍是上下分区，判为未通过。
- 网格的栏线能解释主要元素的起止位置，强调色至少连接两个不同类别的元素，而不是孤立装饰。
- 解释注释模式中的任意规则线或引线都不穿过可读文字；注释线的起点、折点和终点均可解释，且目标构件唯一。
- 每一处文字—文字或文字—建筑重叠都能说出共同轴线、前后顺序和视觉任务；说不出来的重叠必须删除。
- 主体容器、背景尺度和语境材料各不超过一个；字窗保留越界身份锚点，多窗可沿共同轴拼回，纹样只占 1–2 个区域且不吞掉主檐、塔刹、入口或匾额。
- 纯文字参考没有带来虚构诗文、日期、活动、签名、印章或赞助信息；外国参考没有带来异国建筑、宗教符号、人物、徽章、纹样、品牌或广告。
- 隐去中文地名后，画面仍可凭目标建筑的轮廓、材料、构件或地域色被识别；若只剩“把外国模板换成中文”，判为中式转译失败。
- 页面中没有成组重复的卡片、按钮式年份、投影标签或仪表盘式编号；若去掉容器后层级就消失，说明字体、尺度和网格尚未设计完成。
- 主题文字模式中没有可见线、构件指向、编号式科普或定义句；事实短词已经成为尺度、色彩、反白、节奏或遮挡的一部分。
- 建筑、天空、环境与前景都按材质图发生可见变化；若只有建筑被抠出而天空和背景仍近似原照片，判为未完成。
- 所有附加装饰图形都能同时说明主题来源和构图任务；无法连接至少两个元素、孤立在角落或只是填空的装饰必须删除。
- 使用 `geometry-only` 时只检查主体范围、负空间、色场和遮挡方向，不以它证明文字正确。使用通过门控的 `typeset-guide` 时才比较共享边线、文字块尺度、换行和遮挡方向；若垫图自身未保存通过报告，则本次生成视为流程失败。

若第一次结果只有局部对齐问题，优先修改垫图中的对应边界框、字号或裁切关系，再整体重绘；不要在结果上不断追加补丁文字。每轮只修一个变量并重复建筑不变量，避免主体漂移。

## 按生成前选择输出拼图

不要在交付后才第一次询问拼图。按生成前确认的输出计划执行；用户选择“不需要”时只交付海报，选择“需要”时在全部海报通过验收后使用 `scripts/make_comparison.py`：

- 原图为竖图时默认左右拼，原图在左、海报在右。
- 原图为横图时默认上下拼，原图在上、海报在下。
- 多张海报默认每张分别与原图生成一张拼图，不把多张海报挤进同一个未经确认的长图。
- 默认保留两张图的完整内容，允许成品比例随之改变；若用户要求固定平台比例，再询问是否允许裁切。

```bash
python3 scripts/make_comparison.py ORIGINAL POSTER OUTPUT
```
