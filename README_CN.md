# remotion-video

[English](README.md)

使用 Remotion 框架编程式创建视频的 Claude Code Skill。

## 功能特点

- 使用 React 组件编程式创建视频
- AI 驱动的 TTS 音频生成（MiniMax 或 Edge TTS）
- 基于场景的架构，自动计算时长
- 支持动画、字幕、音乐可视化

## 安装

### Claude Code 用户

将整个 `remotion-video` 文件夹复制到 Claude Code skills 目录：

```bash
git clone https://github.com/wshuyi/remotion-video-skill.git
cp -r remotion-video-skill ~/.claude/skills/remotion-video
```

然后重启 Claude Code 或开启新会话。

### TTS 配置（二选一）

#### 方案 A：Edge TTS（免费，推荐快速上手）

无需配置！Edge TTS 免费且开箱即用。

只需安装 Python 依赖：
```bash
pip install edge-tts
```

#### 方案 B：MiniMax TTS（付费，支持声音克隆）

1. 从 [MiniMax 平台](https://platform.minimaxi.com/) 获取 API 密钥
2. 设置环境变量：

```bash
# 添加到 ~/.zshrc 或 ~/.bashrc
export MINIMAX_API_KEY="你的API密钥"
export MINIMAX_VOICE_ID="你的音色ID"
```

获取 Voice ID：
- 使用 MiniMax 内置音色，或
- 在平台上克隆自己的声音

## 使用方法

安装后，通过以下方式触发：

- "用代码做视频"
- "编程视频"
- "Remotion"
- "/remotion-video"

### 示例提示词

**教程视频：**
> 帮我做一个讲解 Python 装饰器的教程视频，5分钟左右

**数据可视化：**
> 用 Remotion 做一个展示2024年销售数据的动画视频

**音乐可视化：**
> 帮我做一个音乐可视化视频，配合这首歌的节奏

## 项目结构

Skill 创建的项目结构：

```
my-video-project/
├── src/
│   ├── Root.tsx           # 主组合
│   ├── audioConfig.ts     # 场景时长配置（自动生成）
│   └── scenes/            # 场景组件
├── public/
│   └── audio/             # TTS 音频文件
├── scripts/
│   └── generate_audio.py  # TTS 生成脚本
└── package.json
```

## 环境要求

- Node.js 18+
- Python 3.8+（用于 TTS）
- ffprobe（用于检测音频时长）

```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg
```

## 许可证

MIT
