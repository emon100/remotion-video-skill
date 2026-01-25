# remotion-video

[中文文档](README_CN.md)

A Claude Code Skill for creating programmatic videos with Remotion framework.

## Features

- Create videos programmatically with React components
- AI-powered TTS audio generation (MiniMax or Edge TTS)
- Scene-based architecture with automatic timing
- Support for animations, subtitles, and music visualization

## Installation

### For Claude Code Users

Copy this entire `remotion-video` folder to your Claude Code skills directory:

```bash
cp -r remotion-video ~/.claude/skills/
```

Then restart Claude Code or start a new session.

### TTS Setup (Choose One)

#### Option A: Edge TTS (Free, Recommended for Quick Start)

No setup required! Edge TTS is free and works out of the box.

Just install the Python dependency:
```bash
pip install edge-tts
```

#### Option B: MiniMax TTS (Paid, Voice Cloning Support)

1. Get your API key from [MiniMax Platform](https://platform.minimaxi.com/)
2. Set environment variables:

```bash
# Add to your ~/.zshrc or ~/.bashrc
export MINIMAX_API_KEY="your-api-key-here"
export MINIMAX_VOICE_ID="your-voice-id-here"
```

To get a Voice ID:
- Use MiniMax's built-in voices, or
- Clone your own voice on their platform

## Usage

After installation, trigger the skill by saying:

- "用代码做视频"
- "编程视频"
- "Remotion"
- "/remotion-video"

### Example Prompts

**Tutorial Video:**
> 帮我做一个讲解 Python 装饰器的教程视频，5分钟左右

**Data Visualization:**
> 用 Remotion 做一个展示2024年销售数据的动画视频

**Music Visualization:**
> 帮我做一个音乐可视化视频，配合这首歌的节奏

## Project Structure

When the skill creates a new project:

```
my-video-project/
├── src/
│   ├── Root.tsx           # Main composition
│   ├── audioConfig.ts     # Scene timing (auto-generated)
│   └── scenes/            # Scene components
├── public/
│   └── audio/             # TTS audio files
├── scripts/
│   └── generate_audio.py  # TTS generation script
└── package.json
```

## Requirements

- Node.js 18+
- Python 3.8+ (for TTS)
- ffprobe (for audio duration detection)

```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg
```

## License

MIT
