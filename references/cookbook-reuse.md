# AI Visual Prompt Cookbook 轻量参考指南

## 目录

1. 使用边界
2. 全局轻量缓存
3. 轻量查找流程
4. 选择与复用规则
5. 常见机制入口
6. 不能直接照搬的内容

## 使用边界

Cookbook 用来快速找到可视化的机制，不是当前 Prompt 必须严格对齐的模板。

- 新项目缺少明确风格、用户要求查找参考，或风格家族改变时才调用。
- 用户已经给出清晰的构图、画面机制和质感目标时，可以不检索 Cookbook。
- 项目记录已有可用的 style slug 且风格未变时，只读记录中的复用结论，不重新打开来源 JSON。
- 实际借用了哪个机制就记录哪个；不要为了形式完整而强行设置主样式和两个辅助样式。

## 全局轻量缓存

- 仓库：<https://github.com/VigoZhao/AI-Visual-Prompt-Cookbook>
- 默认缓存：`${CODEX_HOME:-$HOME/.codex}/cache/image-prompt-director/cookbook`
- 本 skill 最近检查的提交：`29a29a60730d95e5ae59b75de332d93b04680e93`（2026-07-15）
- 当时共有 96 个 `styles/*/style.json`。
- 仓库采用 MIT License。结构与提示词写法归 VigoZhao 原项目；复用时在项目记录保留来源。

缓存只稀疏保留：

```text
README.zh-CN.md
docs/CATALOG.md
schemas/style-v2.1.schema.json
styles/*/style.json
assets/thumbs/*
```

这包含全部结构化提示词和每种风格的一张缩略图，不包含 188 张横竖高清预览、站点、其他语言 README 或项目脚本。不要在每个项目下重新克隆仓库。

当本轮决定调用 Cookbook 时运行一次：

```bash
python3 <skill目录>/scripts/sync_cookbook.py
```

脚本先比较本地与远端 `main` 提交：没有变化则不下载；有变化才以 fast-forward 同步 JSON、目录、schema 和缩略图。网络不可用但缓存完整时继续使用旧缓存，并说明本次未完成更新检查。同一任务只运行一次；未使用 Cookbook 时不运行。

## 轻量查找流程

1. 先在 `README.zh-CN.md`、`docs/CATALOG.md` 和 `style_summary` 中搜索，收敛到 1–3 个候选。
2. 先看缩略图判断媒介、构图和密度是否相符。
3. 只有准备精确复用某个子系统时，才打开对应 `styles/<slug>/style.json`；一般灵感参考不需逐字段比对 canonical JSON。
4. 只在缩略图不足以判断时查看单张高清预览，不下载整库预览。
5. 记录 style slug、缓存提交和实际借用的机制；未采用时只记“本轮未调用”。

本地检索示例：

```bash
CACHE="${CODEX_HOME:-$HOME/.codex}/cache/image-prompt-director/cookbook"
rg -n -i "关键词1|关键词2" "$CACHE/README.zh-CN.md" "$CACHE/docs/CATALOG.md" "$CACHE/styles"
```

只做灵感搜索时可以停在目录、summary 和缩略图；准备声称精确复用某个机制时才回到 canonical `style.json`。

## 选择与复用规则

优先复用以下结构：

- `style_fidelity_anchors`：6–12 个可观察、可检查的风格锁点。
- `visual_deconstruction`：构图逻辑、主体位置、镜头、文字行为和情绪机制。
- `composition`：9:16 与 16:9 的不同组织方式。
- `typography`：字体气质、层级、准确文字、空间参与方式。
- `color_palette`：主色、辅色、强调色及面积比例。
- `image_treatment` 或 `photographic_direction`：匹配插画/渲染或摄影媒介。
- `design_rules`、`do`、`avoid`：从正确机制到残余风险逐级约束。
- `prompt_template`：变量前置、风格锁定、来源边界、比例适配和渲染指令。

默认只借用 1 个最相关的机制，例如构图、文字行为、材质或色彩比例，并把它翻译进当前 render-prompt 的 `style_direction`。不把包含多个 examples 的 canonical JSON 整份当成单幅画面的运行 Prompt。

只有用户明确要创建可复用 style-spec 时，才复制完整 canonical JSON 作骨架，然后：

1. 替换主题、动作、地点、产品、文案和比例。
2. 把上游针对原始来源图的 `source_content_to_avoid` 改成当前参考图的内容边界。
3. 删除与当前机制无关的原始故事、品牌、人物或物件限制。
4. 保留构成风格家族的构图、字体、色彩、材质和密度规则。
5. 完整重写 `current-test`；两个 controlled variant 只保留最小 5 个变量。

需要辅助样式时，它只借一个明确子系统。不要整份拼接，也不要因为参考库字段详细就把所有内容搬入当前 Prompt。

## 常见机制入口

| 需求机制 | 可先查的 slug |
| --- | --- |
| 黑白肖像 + 巨型字体 | `mono-noir-type-portrait-poster-style` |
| 中文字体作为透视空间 | `blue-chinese-perspective-type-canyon-style` |
| 中文商业产品冲击图 | `warm-fisheye-product-impact-ad-style` |
| 玩具感 3D 社交 campaign | `sunny-3d-avatar-campaign-style` |
| 实景照片 + 涂鸦/IP 贴纸 | `playful-mascot-doodle-snapshot-style` |
| 安静高端产品目录 | `quiet-luxury-furniture-nameplate-poster-style` |
| 物件组装成隐喻轮廓 | `halftone-assemblage-metaphor-psa-poster-style` |
| 饮料飞溅 + 多色商业系统 | `multi-color-beverage-splash-ad-system-style` |
| 漫画食物/产品 zine | `yellow-black-manga-food-zine-ad-style` |
| 安静模拟未来编辑感 | `soft-analog-future-editorial-poster-style` |
| 动势摄影拼贴 | `kinetic-editorial-photo-collage-style` |
| 极简三色硬切肖像 | `tri-color-hardcut-portrait-poster-style` |
| 宠物动画草图/分镜感 | `rough-animation-pet-sketch-storyboard-style` |
| 产品技术规格板 | `monochrome-grid-sneaker-tech-spec` |

## 不能直接照搬的内容

- 原图人物身份、品牌、商标、平台 UI、二维码、水印、创作者签名。
- 原样式的具体标题、口号、价格、日期、故事前提和独特物件组合。
- 只对原图成立的 `source_content_to_avoid`。
- 名义上参考风格、实际上复刻原图构图、姿态和文字顺序的组合。

复用目标是保留视觉系统，生成同一家族的新作品。
