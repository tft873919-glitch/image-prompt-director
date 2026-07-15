# 美术指导风格语言

## 使用方式

风格未定时，先在 [style-library.md](style-library.md) 中按品类、情绪、媒介、配色或版式词查询，收敛到 1–3 个候选词族。这里负责把候选进一步翻译为模型可执行的专业语言；不要直接输出词库中的宽泛分类。

把抽象审美要求翻译成模型可执行的英文术语和可见后果。使用结构：

`[primary medium/style] × [composition or typography influence] × [material/optical influence]`

风格配方不是关键词串。主风格负责全局语法；每个辅助影响只负责一个子系统。如果一个词无法对应到形状、密度、边缘、光学、材质、字体或空间中的可见变化，就删掉。

## 多风格合成示例

**安静高端产品海报**

- 配方：`quiet luxury editorial still life × monumental Swiss typography × tactile material realism`
- 主风格：`quiet luxury editorial still life` 控制低密度、克制色调、产品位置和安静空间。
- 辅助 1：`monumental Swiss typography` 只控制字号对比、网格和边缘裁切。
- 辅助 2：`tactile material realism` 只控制织物、木纹和漫反射光。
- 统一规则：三者共用低饱和、大块面和精确边缘。

**动态文化海报**

- 配方：`kinetic editorial photo collage × condensed grotesk typography × dry-brush motion grammar`
- 主风格控制照片分层、对角线重心和大面积留白；字体只控制黑色窄体块；干笔只承担运动方向，不覆盖全画面。

**实验性中文字体海报**

- 配方：`spatial Chinese typography × one-point perspective architecture × hard-edge screenprint color blocking`
- 字体是空间主体，透视建筑只给字体深度，丝网印刷只控制色块和边缘。不再加写实人物和电影光。

## 普通说法 → 美术指导说法

### 高级留白

- 弱：“大量高级留白，简洁大气。”
- 强：`asymmetric editorial negative space` ；主体压在右下约三分之一，左上留出一块连续竖向负形，标题只占其底部，留白用来放大产品的孤立与克制。

### 冲击力

- 弱：“画面更震撼、更有冲击力。”
- 强：`extreme near-field scale contrast, low-angle wide-lens perspective, aggressive edge crop`；前景主体超出画布边缘，背景信息被压到小尺度，冲击来自大小块与透视，不靠爆炸光和颗粒。

### 质感

- 弱：“材质细腻，质感高级。”
- 强：`macro material fidelity, grazing side light, controlled specular width, tactile surface variation`；织物保留长短毛方向，胡桃木反射为宽而暗的高光，金属边缘出现窄亮带，不使用统一塑料光泽。

### 动感

- 弱：“更有速度感和运动感。”
- 强：`diagonal center of gravity, off-axis crop, directional motion blur, shutter-drag edge echo`；清晰的脸或产品作为锁点，手臂、道具或边缘沿单一方向拉伸，不给全画面均匀模糊。

### 电影感

- 弱：“电影级光影，cinematic。”
- 强：`35mm environmental portrait, motivated practical lighting, low-key exposure, restrained highlight roll-off, shallow but readable depth`；光源来自画内门缝或灯箱，环境保留可读暗部，不加无动机蓝橙轮廓光。

### 设计感

- 弱：“更有设计感，排版更高级。”
- 强：`strict modular grid with one deliberate break, controlled scale jump, optical alignment, edge-aware cropping`；大部分元素服从同一网格，只让主标题或主体突破一次，不用随机 icon 和装饰线代替设计。

### 拼贴感

- 弱：“多种风格混合，层次丰富。”
- 强：`editorial photomontage with a single cut-edge language`；所有照片共用同一切边、颗粒和影调，图形层只负责连接视线，材质层只负责统一表面。不让每张参考图都保留自己的媒介语法。

## 风格冲突快速判断

- 摄影写实与平面矢量可组合，但要明确谁是主体媒介，另一方只作平面层。
- 低密度 quiet luxury 与高密度 zine/collage 不能平均融合；只能一方主导，另一方贡献局部字体或边缘。
- 柔和漫反射材质与高强镜面反射必须分区，不要全场同时发生。
- 手工错位、粗糙纸纹与完美无瑕的超现实 3D 需要一个明确的层级转换，否则会显得是滤镜拼贴。

最终只保留一条能读出主次的 style formula，不把所有候选词塞进 Prompt。
