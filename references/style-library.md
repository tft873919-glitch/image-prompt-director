# 设计风格关键词库

用于前期风格确定和 Prompt 编译时检索候选词族。中英对照，覆盖常见设计风格、配色与构图关键词。它只负责快速找到 1–3 个候选入口；最终风格必须按 [style-language.md](style-language.md) 翻译成有主次的 style formula、子系统角色和可见效果，不能把这里的关键词整串复制进 Prompt。

## 目录

1. 使用边界
2. 主流风格
3. 配色方向关键词
4. 构图与版式关键词
5. 使用建议

## 使用边界

- 风格未定、用户只给出抽象审美词，或风格家族发生变化时才查询。
- 用户已锁定明确风格配方，或小版本只改动作、文字、局部色光材质时，不重复查询。
- 先按 brief 中的品类、情绪、媒介、配色或版式词用 `rg` 搜索相关段落，通常只保留 1–3 个候选。
- 词库给出的是基础分类和搜索词，不代替美术判断，也不自动触发 Cookbook 检索。

## 主流风格

### 极简 Minimal
- **特征**：大量留白、极少元素、强字体层级、克制配色（常黑白+一色）、功能至上
- **适用**：科技/金融/高端品牌、海报、Logo、UI
- **搜索词**：`minimal design`、`minimalist poster`、`clean layout`、`negative space`

### 扁平 Flat
- **特征**：无渐变无阴影、纯色块、几何化、明快配色、清晰图标
- **适用**：UI、插画、信息图、社媒配图
- **搜索词**：`flat design`、`flat illustration`、`material flat`

### 毛玻璃 Glassmorphism
- **特征**：半透明磨砂质感、背景模糊、柔和渐变、细边框、层次叠加
- **适用**：UI 卡片、App 视觉、banner
- **搜索词**：`glassmorphism`、`frosted glass UI`、`glassmorphism card`

### 新拟态 Neumorphism
- **特征**：柔和凸起/凹陷、单色系、双重阴影、仿物理质感
- **适用**：UI 控件、仪表盘、App 图标
- **搜索词**：`neumorphism`、`neumorphic UI`、`soft UI`

### 3D / 等距 3D Isometric
- **特征**：立体几何、等距投影、柔和光影、糖果色或金属质感
- **适用**：插画、banner、App 引导页、信息图
- **搜索词**：`3D illustration`、`isometric design`、`3D render poster`、`clay 3D`

### 赛博朋克 Cyberpunk
- **特征**：霓虹光效、暗背景、品红+青蓝撞色、故障艺术、未来感、电子线路
- **适用**：科技活动海报、游戏视觉、音乐封面
- **搜索词**：`cyberpunk poster`、`neon design`、`futuristic neon`、`glitch art`

### 国潮 Guochao / 中国风
- **特征**：传统纹样现代化、书法字体、红金配色、水墨/工笔元素、国色（朱砂/石青/藤黄）
- **适用**：本土品牌、节庆海报、文创、食品包装
- **搜索词**：`国潮设计`、`中国风海报`、`chinese style poster`、`guochao design`、`ink wash modern`

### 日式 / 和风 Japanese
- **特征**：留白、低饱和、细线、竖排文字、和纸纹理、季节感、性冷淡
- **适用**：餐饮、文创、文艺活动、化妆品
- **搜索词**：`japanese design`、`和風デザイン`、`muji style`、`wabi sabi`

### 孟菲斯 Memphis
- **特征**：几何撞色、波点/锯齿/波浪线条、不规则图形、活泼俏皮
- **适用**：年轻品牌、活动 banner、社媒配图、包装
- **搜索词**：`memphis design`、`memphis pattern`、`geometric playful`

### 波普 Pop Art
- **特征**：高饱和撞色、网点、粗黑线、重复排列、消费符号、安迪沃霍尔风
- **适用**：潮流品牌、音乐视觉、活动海报
- **搜索词**：`pop art poster`、`andy warhol style`、`comic style design`

### 渐变 Gradient
- **特征**：多色渐变、流体形状、梦幻过渡、Mesh 渐变、活力科技感
- **适用**：科技品牌、App 视觉、banner、背景
- **搜索词**：`gradient design`、`mesh gradient`、`fluid gradient`、`gradient poster`

### 手绘 / 水彩 Hand-drawn / Watercolor
- **特征**：笔触质感、不均匀上色、纸张纹理、温度感、个人风格
- **适用**：餐饮、文创、婚礼邀请、儿童产品
- **搜索词**：`watercolor illustration`、`hand drawn design`、`手绘插画`、`水彩海报`

### 复古 / 怀旧 Retro / Vintage
- **特征**：做旧质感、暖黄/棕色调、老式字体、胶片颗粒、复古印刷
- **适用**：餐饮、咖啡、酒类、文创、活动
- **搜索词**：`retro poster`、`vintage design`、`复古海报`、`80s retro`、`risograph`

### 双色 / 双色调 Duotone
- **特征**：图片双色处理、强对比、潮流感、单图+撞色叠加
- **适用**：音乐/活动海报、banner、封面
- **搜索词**：`duotone poster`、`duotone design`、`双色调海报`

### 杂志/编辑 Editorial
- **特征**：强网格、衬线大标题、多栏文字、图文混排、高级感
- **适用**：报告封面、品牌画册、时尚/生活方式
- **搜索词**：`editorial design`、`magazine layout`、`editorial poster`

### Y2K / 千禧美学
- **特征**：金属质感、糖果粉、 butterfly 元素、未来复古、闪亮、像素感
- **适用**：潮流时尚、美妆、音乐、Z 世代社媒
- **搜索词**：`y2k aesthetic`、`y2k design`、`2000s retro futuristic`

## 配色方向关键词

| 方向 | 关键词 | 适用 |
|------|--------|------|
| 莫兰迪低饱和 | `muted palette`、`morandi colors`、`earth tones` | 文艺、高级、治愈 |
| 撞色 | `bold contrast`、`complementary colors`、`clash color` | 活力、潮流、活动 |
| 单色 | `monochrome`、`single color`、`one tone` | 极简、高级、专注 |
| 渐变 | `gradient`、`mesh gradient`、`color transition` | 科技、梦幻、活力 |
| 暖色 | `warm tones`、`sunset palette` | 餐饮、温暖、亲和 |
| 冷色 | `cool tones`、`blue palette`、`cyan tech` | 科技、专业、冷静 |
| 黑金 | `black and gold`、`luxury dark` | 奢华、高端、夜场 |
| 国色 | `chinese traditional colors`、`朱砂石青` | 国潮、传统、节庆 |

## 构图与版式关键词

- 留白构图：`negative space`、`minimal layout`、`whitespace`
- 居中对称：`centered layout`、`symmetrical`、`formal balance`
- 不对称平衡：`asymmetrical balance`、`dynamic layout`
- 网格排版：`grid system`、`modular layout`、`swiss style`
- 满版出血：`full bleed`、`edge to edge`、`immersive`
- 对角线动势：`diagonal composition`、`dynamic angle`
- 框中框：`framed composition`、`border layout`

## 使用建议

- **搜索词组合**：主题词 + 风格词 + 类型词，如 `coffee poster minimal negative space`
- **中英并用**：Pinterest/Behance/Dribbble 用英文，花瓣/站酷用中文
- **生图提示词**：不要直接粘贴裸风格词；把候选词翻译成媒介、构图、字体、材质或光学上的可见后果
- **多风格合成**：先锁定 1 个主风格，最多增加 2 个辅助影响；每个辅助影响只负责一个子系统
