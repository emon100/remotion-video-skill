# remotion-video

[English](README.md)

Claude Code Skill - 使用 Remotion 框架编程式创建视频。整合官方最佳实践、中文 TTS 支持和结构化视频创作工作流。

## 特性

- **结构化创作工作流** - 每个场景同时设计音频 + 画面 + 动画
- **多方案文案创作** - 生成 2-3 个不同风格/节奏的方案供选择
- **AI 语音合成** - MiniMax（音色克隆）、Qwen（中文）、Edge TTS（免费）
- **官方规则集成** - 30+ 规则文件来自 [remotion-dev/skills](https://github.com/remotion-dev/skills)
- **公共环境复用** - Python 虚拟环境和 Chrome 缓存复用

## 安装

### Claude Code 用户

将整个 `remotion-video` 文件夹复制到 Claude Code skills 目录：

```bash
git clone https://github.com/wshuyi/remotion-video-skill.git
cp -r remotion-video-skill ~/.claude/skills/remotion-video
```

然后重启 Claude Code 或开启新会话。

### 一次性环境配置

```bash
# 创建 TTS 公共 Python 环境
python3 -m venv ~/.claude/envs/remotion-tts
source ~/.claude/envs/remotion-tts/bin/activate
pip install requests edge-tts dashscope

# 安装系统依赖 (macOS)
brew install ffmpeg node
```

### TTS 配置（选择一种）

| 方案 | 配置 | 优点 | 价格 |
|------|------|------|------|
| **Edge TTS** | 无需配置 | 免费，开箱即用 | 免费 |
| **Qwen TTS** | `DASHSCOPE_API_KEY` | 中文音质优秀 | ¥0.02/千字 |
| **MiniMax** | `MINIMAX_API_KEY` + `MINIMAX_VOICE_ID` | 支持音色克隆 | ¥0.05/千字 |

## 使用方法

触发词：

- "用代码做视频" / "编程视频"
- "Remotion" / "remotion"
- "/remotion-video"

### 示例提示词

**教程视频：**
> 帮我做一个讲解 CNN 卷积神经网络的教程视频，5分钟左右

**个人故事：**
> 帮我把这个经历做成一个短视频，我来提供截图

**数据可视化：**
> 用 Remotion 做一个展示2024年销售数据的动画视频

## Skill 结构

```
remotion-video/
├── SKILL.md           # 主技能文档（工作流 + 参考）
├── rules/             # 官方 Remotion 规则（30+ 文件）
│   ├── animations.md  # 动画基础
│   ├── timing.md      # 时间插值
│   ├── audio.md       # 音频处理
│   └── ...
├── scripts/           # TTS 生成脚本
│   ├── generate_audio_minimax.py
│   ├── generate_audio_qwen.py
│   ├── generate_audio_edge.py
│   └── check-env.sh   # 环境检查
└── templates/
    └── audioConfig.ts
```

## 规则文件索引

常用任务对应的规则文件：

| 任务 | 规则文件 |
|------|----------|
| 动画 | `rules/animations.md`, `rules/timing.md` |
| 视频/音频 | `rules/videos.md`, `rules/audio.md` |
| 字幕 | `rules/subtitles.md`, `rules/display-captions.md` |
| 3D 内容 | `rules/3d.md` |
| 过渡效果 | `rules/transitions.md` |
| 图表 | `rules/charts.md` |

## 系统要求

- Node.js 18+
- Python 3.8+
- ffmpeg/ffprobe

```bash
# macOS
brew install ffmpeg node

# Ubuntu/Debian
sudo apt install ffmpeg nodejs
```

## 致谢

- 官方规则来自 [remotion-dev/skills](https://github.com/remotion-dev/skills)
- Remotion 框架 by [Remotion](https://remotion.dev)

## 许可证

MIT
