---
name: remotion-video
description: |
  使用 Remotion 框架以编程方式创建视频。Remotion 让你用 React 组件定义视频内容，支持动画、字幕、音乐可视化等。
  触发词：
  - "用代码做视频"、"编程视频"、"React 视频"
  - "Remotion"、"remotion"
  - "/remotion-video"
  适用场景：
  - 程序化视频：(1) 批量生成 (2) 数据驱动（如年度总结）(3) 音乐可视化 (4) 自动字幕
  - 教程讲解视频：(5) 技术概念可视化（如 CNN、算法）(6) 分层递进讲解 (7) AI 配音教程
  - 3D 视频：(8) 产品展示/模型动画 (9) 卡通角色讲解 (10) 3D 数据可视化 (11) Logo 动画
---

# Remotion Video

用 React 以编程方式创建 MP4 视频的框架。

## 详细规则文件索引

根据具体需求，加载对应的规则文件获取详细代码示例：

### Remotion API
- [rules/animations.md](rules/animations.md) - 动画基础：必须使用 `useCurrentFrame()` 驱动
- [rules/timing.md](rules/timing.md) - 时间插值：interpolate、spring、easing 曲线
- [rules/sequencing.md](rules/sequencing.md) - 时间编排：延迟、裁剪、限制时长
- [rules/trimming.md](rules/trimming.md) - 裁剪动画的开头或结尾
- [rules/transitions.md](rules/transitions.md) - 场景过渡效果

### 媒体资源
- [rules/assets.md](rules/assets.md) - 导入图片、视频、音频、字体
- [rules/images.md](rules/images.md) - 使用 `<Img>` 组件嵌入图片
- [rules/videos.md](rules/videos.md) - 嵌入视频：裁剪、音量、速度、循环、音高
- [rules/audio.md](rules/audio.md) - 音频处理：导入、裁剪、音量、速度、音高
- [rules/fonts.md](rules/fonts.md) - 加载 Google Fonts 和本地字体
- [rules/gifs.md](rules/gifs.md) - 与时间轴同步的 GIF 显示

### 字幕与文字
- [rules/subtitles.md](rules/subtitles.md) - 字幕和 Caption 概览
- [rules/transcribe-captions.md](rules/transcribe-captions.md) - 转录音视频生成字幕
- [rules/display-captions.md](rules/display-captions.md) - 显示字幕
- [rules/import-srt-captions.md](rules/import-srt-captions.md) - 导入 SRT 字幕文件
- [rules/text-animations.md](rules/text-animations.md) - 文字排版和动画
- [rules/measuring-text.md](rules/measuring-text.md) - 测量文字尺寸、适配容器

### 视觉效果
- [rules/charts.md](rules/charts.md) - 图表和数据可视化
- [rules/lottie.md](rules/lottie.md) - 嵌入 Lottie 动画
- [rules/light-leaks.md](rules/light-leaks.md) - 光晕叠加效果
- [rules/transparent-videos.md](rules/transparent-videos.md) - 渲染透明背景视频
- [rules/maps.md](rules/maps.md) - 使用 Mapbox 添加地图并动画化

### 3D / Composition / 媒体工具
- [rules/3d.md](rules/3d.md) - Three.js + React Three Fiber 创建 3D 内容
- [rules/compositions.md](rules/compositions.md) - 定义 Composition、静态图
- [rules/calculate-metadata.md](rules/calculate-metadata.md) - 动态设置时长、尺寸
- [rules/parameters.md](rules/parameters.md) - 使用 Zod Schema 参数化视频
- [rules/get-audio-duration.md](rules/get-audio-duration.md) / [get-video-duration.md](rules/get-video-duration.md) / [get-video-dimensions.md](rules/get-video-dimensions.md) - 获取媒体时长和尺寸
- [rules/tailwind.md](rules/tailwind.md) - 在 Remotion 中使用 TailwindCSS

### 视频架构与风格（自定义）
- [rules/tts-providers.md](rules/tts-providers.md) - TTS 提供商详情（MiniMax/Qwen/Edge/火山引擎）+ 音频后处理
- [rules/tutorial-architecture.md](rules/tutorial-architecture.md) - 教程类视频：场景驱动架构、Hook、相机控制
- [rules/dialogue-video.md](rules/dialogue-video.md) - 对话式视频：多层架构、ChatOverlay、术语浮窗
- [rules/3b1b-style.md](rules/3b1b-style.md) - 3Blue1Brown 风格：配色、逐步构建、探索式脚本
- [rules/process-animation.md](rules/process-animation.md) - 过程动画：计算步骤、滑动窗口、数值飞入

---

## 视频创作工作流

```
1. 需求收集 → 2. 文案创作（2-3方案）→ 3. 用户选择 → 4. 素材清单 → 5. 语音生成 → 6. 视频开发 → 7. 渲染
```

### 第一步：文案设计（最重要）

每个场景必须同时设计：**语音脚本**（讲什么）、**视觉元素**（看什么）、**镜头感**（画面如何变化）。

开发前必须向用户确认：素材是否齐全、缺失素材能否提供、是否用动画代替实拍、视觉风格偏好。

### 第二步：提供2-3个文案方案

| 方案 | 风格 | 节奏 | 时长 | 适合场景 |
|------|------|------|------|----------|
| A | 快节奏 | 信息密集，画面切换快 | 1-2分钟 | 短视频、产品展示 |
| B | 故事型 | 起承转合，情感递进 | 3-5分钟 | 个人故事、品牌宣传 |
| C | 教程型 | 分步讲解，留白思考 | 5-10分钟 | 技术教程、知识科普 |

### 第三步：确认素材清单

分为三类：用户必须提供（截图、录屏、Logo）、可选提供（背景音乐、真人出镜）、开发者制作（动画、图表、文字动效）。

---

## 环境配置

```bash
# 依赖
brew install node ffmpeg        # macOS
npm install msedge-tts          # Edge TTS（免费）

# Chrome Headless（可选，用系统 Chrome 避免重复下载）
export PUPPETEER_EXECUTABLE_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
```

推荐 package.json scripts：`dev` (remotion studio)、`audio` (TTS 生成)、`render` (视频渲染)、`check-env` (环境检查)。

---

## 核心概念

| 概念 | 作用 |
|------|------|
| `Composition` | 视频定义：尺寸、帧率、时长 |
| `useCurrentFrame()` | 获取当前帧号，驱动一切动画 |
| `interpolate()` | 帧号 → 任意值（位置、透明度等） |
| `spring()` | 物理弹性动画 |
| `<Sequence>` | 时间轴上排列组件 |
| `<AbsoluteFill>` | 全屏定位容器 |

创建项目：`npx create-video@latest`，启动预览：`npm run dev`。

项目结构：`src/Root.tsx`（注册 Composition）、`src/*.tsx`（视频组件）、`public/`（静态资源）。

---

## AI 语音配音

### TTS 方案选择

| 方案 | 优点 | 价格 | 推荐场景 |
|------|------|------|----------|
| **火山引擎 Seed-TTS** | 音质最佳，200+音色，多系列 | ¥0.02-0.05/千字 | 中文多角色视频首选 |
| **MiniMax TTS** | 支持音色克隆 | ¥0.05-0.1/千字 | 需要特定音色 |
| **Qwen TTS** | 多种预置音色 | ¥0.02-0.04/千字 | 中文视频 |
| **Edge TTS** | 免费无需配置 | 免费 | 快速测试 |

详细配置和代码见 → [rules/tts-providers.md](rules/tts-providers.md)

### 火山引擎关键要点

- API 端点：`https://openspeech.bytedance.com/api/v3/tts/unidirectional`
- **音色与 resource_id 必须匹配**：uranus → `seed-tts-2.0`，moon → `seed-tts-1.0`（不匹配返回空音频无报错！）
- 响应是流式 JSON Lines，音频在 `data` 字段（不是 `audio`）
- 成功码：`0` 和 `20000000` 都是成功

### 音频后处理（必做）

TTS 生成的音频通常需要：去首尾静默 + 调整语速 + 片头音乐淡出。

- **去静默+加速**：`ffmpeg -af "silenceremove=...,areverse,silenceremove=...,areverse,atempo=1.2"`
- **片头淡出**：`ffmpeg -af "afade=t=out:st=5:d=3" -t 8`
- **更新时长**：处理后用 `ffprobe` 获取实际时长，`ceil(时长) + 1s` 更新 audioConfig

详细命令见 → [rules/tts-providers.md](rules/tts-providers.md)（底部"音频后处理"章节）

---

## 视频架构选择

### 教程类：场景驱动架构

核心：`audioConfig.ts` 是单一数据源，音频决定时长，一个概念 = 一个场景。

用 `useCurrentSceneIndex()` Hook 根据帧号返回当前场景索引，所有层根据索引渲染内容。

详细代码见 → [rules/tutorial-architecture.md](rules/tutorial-architecture.md)

### 对话式：多层分工架构

6 层结构：背景 → 场景主画面 → 对话气泡/字幕 → 全局 UI → 术语浮窗 → 音频 → 进度条。

关键组件：
- **ChatOverlay**：根据 speaker 切换气泡方向和颜色
- **SubtitleBar**：结尾场景居中半透明字幕条
- **TermGlossaryLayer**：术语解释通知弹窗，`useMemo` 预计算绝对帧，最多同时 2 个

详细代码见 → [rules/dialogue-video.md](rules/dialogue-video.md)

---

## 视频节奏控制

节奏是视频质量的核心。

### TTS 语速

| 场景类型 | 推荐倍速 |
|---------|---------|
| 日常对话 | 1.2x |
| 技术讲解 | 1.0x-1.1x |
| 情绪表达/旁白 | 1.0x-1.15x |

### 长短句交替

用短反应句（2-5s）打断长段落，制造呼吸感。理想分布：短句 40%、中等 35%、长句 25%。长句超过 40% 观众容易走神。

### 叙事弧线

- **片头（0-15s）**：品牌 5-8s（不超过 10s）→ 钩子前置（先抛吸引点，再讲背景）
- **中段**：信息密度波动，诊断/修复高密度 + 用户反应短句穿插喘息
- **收尾（最后 20s）**：总结 → 反应 → 金句（2-3s，极短，记忆锚点）→ CTA 引导

### 片头音乐

5s 满音量 + 3s 渐弱淡出，在第一句配音前必须已经淡出，不与配音重叠。

### 真实素材速度

| 素材类型 | 推荐速度 |
|---------|---------|
| 终端操作 | 2x-3x |
| GUI 录屏 | 1.5x-2x |
| 效果展示 | 1x-2x |

用 `<OffthreadVideo playbackRate={2} />` 控制。

### 场景过渡

对话式视频的转场在对话本身，不需要花哨视觉转场。话题切换用一句过渡语自然衔接。

### 节奏自检清单

- [ ] 前 5s 有足够吸引力？
- [ ] 有没有超过 15s 的单段独白？
- [ ] 短句占比 30% 以上？
- [ ] 全片有 2-3 个爽点？
- [ ] 金句够短且有记忆点？
- [ ] 音乐在配音前已淡出？
- [ ] 演示素材加速过？
- [ ] TTS 语速调整过（至少 1.1x）？

---

## 3Blue1Brown 风格

让观众「自己发现」，而不是「被告知答案」。Why → What，逐步构建，颜色有语义，数值具象化，2D 优先。

脚本用探索式而非宣布式：先提问引发思考，再逐步展示机制。

详细配色、组件、脚本模板见 → [rules/3b1b-style.md](rules/3b1b-style.md)

---

## 过程动画模式

展示「怎么算」而非「是什么」：逐步计算、数值飞入、区域比较、滑动窗口。

脚本关键：给动画留白时间。首次完整展示（3-4s/步）→ 后续加速（0.5s/步）。

详细组件和时间分配见 → [rules/process-animation.md](rules/process-animation.md)

---

## 3D 视频（@remotion/three）

安装：`npm i three @react-three/fiber @remotion/three @types/three`，模板：`npx create-video@latest --template three`。

适用：产品展示、角色动画、数据可视化、Logo 动画。

关键点：
- 用 `<ThreeCanvas>` 包裹 3D 内容
- 用 `sceneIndex` 条件渲染避免 WebGL 上下文溢出
- 渲染配置加 `--gl=angle`
- `useGLTF` 加载 GLTF 模型，`useOffthreadVideoTexture` 做视频纹理
- 用基础几何体（球+胶囊+圆柱）组合卡通角色，无需专业建模

模型资源：Mixamo（骨骼动画）、Sketchfab（3D 模型）、Spline（在线 3D 设计）、gltfjsx（GLTF→React）

详细 3D API 见 → [rules/3d.md](rules/3d.md)

---

## 渲染

```bash
npx remotion render src/index.ts CompositionId --codec=h264 --concurrency=2
```

| 参数 | 说明 |
|------|------|
| `--codec` | h264, h265, vp8, vp9, gif, mp3, wav |
| `--crf` | 质量 (0-51，越小越好，默认18) |
| `--scale` | 缩放因子（测试用 0.5） |
| `--concurrency` | 并行数（有视频素材时用 2，纯动画可用 4） |
| `--gl` | 3D 场景用 `angle` |

高级：字幕用 `@remotion/captions` + Whisper，Web 嵌入用 `@remotion/player`，分布式用 `@remotion/lambda`。

---

## 渲染踩坑经验

| 问题 | 原因 | 解决 |
|------|------|------|
| 画面抖动/闪烁 | `React.lazy()` 写在组件函数内 | **必须放在模块级别** |
| 视频丢帧 | 使用了 `<Video>` | 改用 `<OffthreadVideo>` |
| 渲染内存溢出 | 大图片（4032×3024） | ffmpeg 缩放到 1920 宽度 |
| 渲染崩溃 | `--concurrency` 太高 | 含视频素材时用 `--concurrency=2` |
| WebGL 上下文溢出 | 多 3D 场景同时存在 | sceneIndex 条件渲染 + `--gl=angle` |
| 相机持续抖动 | `pos += (target-pos)*factor` 不收敛 | 直接设置或用 spring |
| 网格图像旋转90度 | row/col 坐标映射反了 | col→x, row→y（翻转） |
| 进度值好几千% | progress 变量未 clamp | `Math.min(1, ...)` |

---

## 工作流最佳实践

1. **前台执行**：音频生成和渲染务必前台运行以显示进度
2. **断点续作**：批量任务检查已存在文件跳过，单文件失败不影响整体
3. **幂等执行**：重复运行产生相同结果
4. **调试**：Studio 热重载 `npm run dev`，拖动时间轴逐帧检查
5. **性能**：组件内重计算用 `useMemo`，静态文件放 `public/` 用 `staticFile()`

---

## 参考资源

- 官方文档：https://remotion.dev/docs
- 模板库：https://remotion.dev/templates
- GitHub：https://github.com/remotion-dev/remotion
