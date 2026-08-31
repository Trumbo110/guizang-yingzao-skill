# 建筑海报 Design Token 系统

本系统把 [design-element-library.md](design-element-library.md) 中的设计判断编码成稳定、可检索、可组合的 Token。它借用 Design System 的分层思想，但不把开放设计降格成固定模板：Token 负责限定角色、关系和边界，具体尺寸、字形与构图仍由目标照片决定。

机器可读清单位于 [design-tokens.json](design-tokens.json)，逐图来源证据仍保留在参考编码文档中。

## 四层模型

1. **Primitive**：可计算的基础尺度，例如栏数、外边距、沟槽、字级比例、遮挡比例和 z 值。Primitive 不单独决定风格。
2. **Semantic**：回答“它在画面里负责什么”，例如中文展示标题、资料字、背景尺度、身份保护、地域强调色。
3. **Component**：可复用的视觉机制，例如字窗纪念碑、连续竖窗、来源正文场、纹样边缘遮罩和细网点建筑。
4. **Recipe**：已经过兼容检查的一组 Token；它是起点而非模板，仍需根据照片替换主体范围、文案、取色和材质参数。

Token ID 使用 `cap.<category>.<name>`：

```text
cap.primitive.grid-6
cap.type.display-cn
cap.layout.type-window
cap.material.arch-halftone-fine
cap.depth.arch-over-ghost-type
cap.policy.no-visible-lines
```

ID 是稳定接口。可以扩写描述和标签，但不要因措辞变化重命名；确需废弃时增加别名或迁移记录。

## Token 契约

每个 Token 至少包含：

```json
{
  "id": "cap.layout.type-window",
  "tier": "component",
  "category": "layout",
  "label": "字窗纪念碑",
  "intent": "让短标题同时成为图像容器和背景尺度",
  "value": { "subject_inside": "60-75%", "identity_breakout": "25-40%" },
  "tags": ["塔", "门楼", "短标题", "字窗"],
  "requires": ["cap.type.display-cn", "cap.subject.identity-protection"],
  "compatible": ["cap.material.arch-duotone", "cap.depth.identity-breakout"],
  "conflicts": ["cap.layout.multi-image-collage"],
  "constraints": ["标题限 2-5 个汉字", "至少一个身份锚点越出蒙版"],
  "prompt": "Use the verified short Chinese title as an image mask...",
  "visual": { "glyph": "字", "swatch": "linear-gradient(...)" },
  "sources": ["127c...jpg", "7a760...jpg"]
}
```

- `intent` 解释视觉任务，禁止只写风格形容词。
- `value` 存放可视化和前端可消费的参数；范围优先于伪精确值。
- `requires` 是硬依赖；解析后若缺失，方案无效。
- `compatible` 是加分关系，不代表必须同时选择。
- `conflicts` 是硬冲突，任何方向声明都视为双向冲突。
- `constraints` 是必须进入蓝图或验收的自然语言边界。
- `prompt` 是提示词片段，不包含具体建筑名、虚构事实或外国文化内容。
- `visual` 只用于目录预览，不参与生成判断。
- `sources` 提供参考图证据；它不是复制许可。

## 互斥槽位

`design-tokens.json` 中的 `mutex_groups` 是 Recipe 的主要骨架：

| 槽位 | 上限 | 说明 |
| --- | --- | --- |
| `slot.subject-container` | 1 | 字窗、连续竖窗、同轴多窗、模块拼贴只能选一种 |
| `slot.background-scale` | 1 | 来源正文场、重复短地名、尺度数字只能选一种 |
| `slot.context-material` | 1 | 地形频率场、地域纹样、可信档案层只能选一种 |
| `slot.expressive-type` | 1 | 书写标题、随形文字、巨型几何字只能选一种 |
| `slot.line-policy` | 1 | 主题无可见线与解释注释线不能并存 |

互斥只限制同类主机制。基础纸纹、资料字体、身份保护、区域材质和 z 轴关系可作为依赖加入。

## 解析顺序

1. **检索**：用目标照片标签查询候选，例如 `塔 + 中轴 + 天空留白 + 历史建筑`。
2. **过滤**：删除 `avoid_when` 命中、没有事实来源或没有照片几何对应的 Token。
3. **占槽**：每个互斥槽位先选主导 Token，再解析硬依赖。
4. **冲突检查**：任一 `conflicts` 命中即淘汰，不用提示词“折中”。
5. **兼容评分**：同标签、显式兼容和共同轴线加分；竞争主语义、文化来源不明和身份风险扣分。
6. **中式转译**：外来参考只保留机制，中文语义、建筑几何、地域材料和事实内容全部由目标对象接管。
7. **编译**：将选中 Token 的 `value + constraints + prompt` 写入构图蓝图和生成提示词。
8. **验收**：保留选中 Token ID，逐项检查其约束，不凭“整体感觉还行”跳过失败项。

建议评分：目标几何直接匹配 `+3`，显式兼容 `+2`，同一真实内容来源 `+1`；弱适配 `-2`，文化来源不明 `-3`，显式冲突或身份锚点风险直接淘汰。分数只用于排序，不能覆盖硬约束。

## Recipe 解析

Recipe 由 `tokens`、`optional`、`forbidden` 和 `invariants` 组成：

- `tokens` 是默认必须解析的组合。
- `optional` 只有命中照片与事实条件时才能加入。
- `forbidden` 防止常见模板残留。
- `invariants` 是该组合成立的最小条件。

使用 Recipe 时先把它展开为 Token ID，再根据当前照片删除不适用的可选项；不要把 Recipe 名直接写进图像提示词。

## 可视化与命令行检索

使用 [scripts/design_tokens.py](../scripts/design_tokens.py)：

```bash
python3 scripts/design_tokens.py validate
python3 scripts/design_tokens.py query --category layout --tag 塔
python3 scripts/design_tokens.py query --compatible-with cap.layout.type-window
python3 scripts/design_tokens.py recipe cap.recipe.tower-type-window
python3 scripts/design_tokens.py render --output /tmp/cap-token-catalog.html
```

HTML 目录按层级和类别显示色片、ID、标签、意图、依赖、兼容和冲突，并提供关键词、类别与层级过滤。它是检索界面，不是网页式海报模板。

## 扩展规则

新增参考图时：

1. 先逐图编码事实观察和中式转译。
2. 搜索现有 Token；同一视觉任务优先补 `sources`、标签或约束，不新建同义 Token。
3. 只有出现新的可复用视觉任务时才新增 Token。
4. 新 Token 必须至少加入一个检索标签，声明互斥槽位或说明为何不互斥，并有一条可验收约束。
5. 修改后运行 `design_tokens.py validate` 和 Skill 的 `quick_validate.py`。

不要为每张参考图创建一个 Token，也不要把“高级、复古、东方、氛围感”这类不可执行形容词当 Token。
