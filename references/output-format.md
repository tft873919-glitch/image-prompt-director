# 纯 Prompt 与项目记录

## 目录

1. 输出模式
2. 目录与文件
3. render-prompt JSON
4. 项目记录
5. 可选 style-spec
6. 1000 字符版
7. 版本与验收

## 输出模式

默认使用 **render-prompt**：一份 JSON 只定义当前一幅画面，整文件可直接投喂生图模型。不包含备选画面、controlled variants、项目记录或需要读取其他 Prompt 才成立的补丁。

只有用户明确要建立可跨主题复用的风格模板时，才使用 **style-spec**：遵循 AI Visual Prompt Cookbook v2.1，允许多个 examples 证明风格可迁移性。style-spec 是风格资产，不是默认单次生图输入。

## 目录与文件

```text
prompt/<中文项目名>/
├── <中文项目名>_记录.md
├── <中文项目名>_v1.0.0.md
├── <中文项目名>_v1.0.0_1000字符.md       # 仅需要时
└── <中文项目名>_风格规格_v1.0.0.md      # 仅 style-spec 模式

outputs/<中文项目名>/
├── <中文项目名>_v1.0.0.png
└── <中文项目名>_v1.0.0_02.png
```

保留有意义的中文项目名，只替换路径非法字符。版本文件名不加时间；时间统一放在记录文件。

Prompt 文件必须：

- 第一非空字符是 `{`，最后一非空字符是 `}`。
- 只含一个 JSON 对象；不使用标题、frontmatter、解释、变更记录或代码围栏。
- 完整、独立、可单独投喂。禁止“保持上一版”“沿用旧版”“其余不变”“详见之前 Prompt”。
- 一个要求只设一个主归属字段，不为了字段完整而重复整句。

## render-prompt JSON

字段键名使用英文；内容默认使用准确中文，但 `style_direction` 中的风格、媒介、摄影、材质和排版术语优先使用英文。

```json
{
  "prompt_name": "中文项目名",
  "prompt_version": "1.0.0",
  "format": {
    "type": "海报 / KV / 产品广告 / 社交配图",
    "aspect_ratio": "9:16",
    "use_case": "投放或观看场景"
  },
  "creative_direction": {
    "visual_thesis": "可被画出来的视觉命题",
    "dominant_move": "唯一主导决定",
    "supporting_moves": ["1–2 个支撑决定"],
    "deliberate_sacrifice": "主动牺牲什么",
    "anti_generic": ["只保留与当前项目有关的 1–3 个模型俗套"]
  },
  "style_direction": {
    "style_formula": "primary style × typography/composition influence × material/optical influence",
    "primary_style": {
      "english_terms": ["model-sensitive English style terms"],
      "role": "控制整体媒介、空间、密度和情绪",
      "visible_effect": "具体可见后果"
    },
    "secondary_influences": [
      {
        "english_terms": ["one focused influence"],
        "role": "只控制 typography / material / motion / lighting 中的一项",
        "visible_effect": "具体可见后果"
      }
    ],
    "coherence_rule": "用哪个共同网格、明度、边缘或制作逻辑防止拼凑"
  },
  "scene": {
    "subject": "主体与识别锚点",
    "action": "正在发生的具体瞬间",
    "environment": "场景",
    "product_or_props": "产品或道具；没有时写无",
    "spatial_relationship": "主体、产品、文字和环境的物理关系"
  },
  "visual_hierarchy": {
    "first_glance": "0.5 秒第一眼",
    "second_read": "2 秒第二层信息",
    "detail_reward": "5 秒细看奖励"
  },
  "composition": {
    "camera_and_perspective": "镜头距离、视角、透视与焦点",
    "mass_and_scale": "画面重心、大小块对比和主体尺度",
    "negative_space": "留白的位置、形状和功能",
    "crop_and_edges": "裁切、出血、边缘张力与禁止覆盖区",
    "depth_and_visual_flow": "前中后景、遮挡、视线与阅读路径"
  },
  "typography": {
    "exact_text": {
      "main_title": "准确文案",
      "secondary_text": "如无则删除该键"
    },
    "type_direction": "英文字体/排版术语与可见形态",
    "placement_and_behavior": "文字的位置、层级，以及它是标题、声音、空间或物体中的哪一种"
  },
  "color_lighting_material": {
    "color_system": "主辅强调色、面积关系和明度节奏",
    "lighting": "光源动机、位置、大小、软硬与曝光行为",
    "material_behavior": "材料如何吸光、反光、形成边缘与不完美",
    "production_finish": "photographic / screenprint / risograph / collage / C4D / paper craft 等制作结果"
  },
  "reference_images": [
    {
      "reference": "图1 / 本地文件名",
      "priority": "high / medium / low",
      "role": "identity / product / composition / visual-style / typography / material-lighting",
      "learn": "只学什么",
      "preserve": "必须保留的锚点",
      "do_not_copy": "不复制什么"
    }
  ],
  "hard_constraints": ["少而确定的硬限制"],
  "negative_prompt": "只保留对当前画面高风险的排除词"
}
```

规则：

- `style_formula` 必须含英文模型敏感术语。
- `secondary_influences` 可为空，最多 2 个；不为了显得复杂而凑风格。
- `exact_text` 只放准确出现在画面中的文案；无文字画面可为空对象。
- `reference_images` 可为空；如有参考图，每张图只设一个主要角色并明确优先级。
- `hard_constraints` 和 `negative_prompt` 可为空，不凑条数。
- 不设字符下限；通常不超过 12,000 个 Unicode 字符，复杂项目可按需超出。

## 项目记录

每个项目只维护一个 `<中文项目名>_记录.md`，持续更新，不按版本复制。

```markdown
# <中文项目名>｜创作记录

## 当前状态
- 当前 Prompt：[v1.0.0](./<项目名>_v1.0.0.md)
- 格式模式：render-prompt / style-spec
- 当前成果：无
- 状态：讨论中 / 已锁版 / 已生图 / 待反馈

## Brief 与不可动项
- 传播任务：
- 受众与观看场景：
- 准确文案：
- 必须保留 / 禁止改变：

## 美术指导拍板
- 视觉命题：
- 风格配方：
- 主导决定 / 支撑决定：
- 0.5 秒 / 2 秒 / 5 秒阅读顺序：
- 反默认：
- 明确舍弃：

## 参考图分工
| 参考图 | 路径/附件 | 优先级 | 主要角色 | 学习项 | 保留锚点 | 禁用项 |
| --- | --- | --- | --- | --- | --- | --- |

## Cookbook 复用
| style slug | 查看时间/提交 | 借用机制 | 舍弃内容 |
| --- | --- | --- | --- |

## 版本与反馈
| 版本 | 时间 | 类型 | Prompt | 修改假设/主要变化 | 出图反馈 | 成果 |
| --- | --- | --- | --- | --- | --- | --- |

## 待确认
- 无 / 尚未拍板的问题
```

记录只写过程、判断、拍板和索引，不复制整份 Prompt JSON。

## 可选 style-spec

用户明确要可复用风格模板时，文件名使用 `<项目名>_风格规格_vX.Y.Z.md`，严格遵循 Cookbook v2.1 顶层字段和 schema。

- 至少 3 个 examples 只用于证明风格可迁移，不代表当前单幅画面。
- 需要生图时，从 style-spec 提取一个当前场景，另行编译成 render-prompt；不把包含多案例的 style-spec 默认直接投喂。
- 优先从全局 Cookbook 缓存的 `schemas/style-v2.1.schema.json` 和候选 `style.json` 复用合法结构。

## 1000 字符版

用户要求字符限制时，从 render-prompt 派生 `<项目名>_vX.Y.Z_1000字符.md`。该文件只含可直接投喂的压缩 Prompt，不含标题、解释、代码围栏或记录，也不得引用长版来补齐指令。

压缩顺序：任务/比例 → 视觉命题 → 风格配方 → 主体动作/锚点 → 构图与注意力顺序 → 准确文字 → 光学/材质 → 参考图角色 → 关键限制。

## 版本与验收

- 同版本多次生成：成果增加 `_02`、`_03`；Prompt 不升级。
- Prompt 内容改变：先升级 Prompt，再生成同版本成果。
- 不覆盖 Prompt、压缩版或成果。
- 文件名版本必须与 `prompt_version` 或 `style_version` 一致。
- render-prompt 只有当前画面，style formula 有英文术语且各影响角色清楚。
- 参考图优先级无冲突，视觉命题、注意力顺序、明确舍弃和反默认都已定义。
- 文件无跨版本引用或差异补丁。

```bash
python3 <skill目录>/scripts/validate_prompt_md.py <Prompt文件>
python3 <skill目录>/scripts/validate_prompt_md.py <1000字符Prompt文件>  # 如有
python3 <skill目录>/scripts/validate_record_links.py <记录文件>
```
