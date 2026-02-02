# remotion-video

[中文文档](README_CN.md)

A Claude Code Skill for creating programmatic videos with Remotion framework. This skill integrates official Remotion best practices with enhanced Chinese TTS support and a structured video creation workflow.

## Features

- **Structured Creation Workflow** - Scene design with audio + visuals + animations
- **Multiple Script Proposals** - Generate 2-3 options with different styles/pacing
- **AI-powered TTS** - MiniMax (voice cloning), Qwen (Chinese), Edge TTS (free)
- **Official Rules Integration** - 30+ rules from [remotion-dev/skills](https://github.com/remotion-dev/skills)
- **Reusable Environment** - Shared Python venv and Chrome cache

## Installation

### For Claude Code Users

Copy this entire `remotion-video` folder to your Claude Code skills directory:

```bash
cp -r remotion-video ~/.claude/skills/
```

Then restart Claude Code or start a new session.

### One-Time Environment Setup

```bash
# Create shared Python environment for TTS
python3 -m venv ~/.claude/envs/remotion-tts
source ~/.claude/envs/remotion-tts/bin/activate
pip install requests edge-tts dashscope

# Install system dependencies (macOS)
brew install ffmpeg node
```

### TTS Setup (Choose One)

| Provider | Setup | Pros | Pricing |
|----------|-------|------|---------|
| **Edge TTS** | None | Free, no API key | Free |
| **Qwen TTS** | `DASHSCOPE_API_KEY` | Excellent Chinese | ¥0.02/1k chars |
| **MiniMax** | `MINIMAX_API_KEY` + `MINIMAX_VOICE_ID` | Voice cloning | ¥0.05/1k chars |

## Usage

Trigger the skill with:

- "用代码做视频" / "编程视频"
- "Remotion" / "remotion"
- "/remotion-video"

### Example Prompts

**Tutorial Video:**
> 帮我做一个讲解 CNN 卷积神经网络的教程视频，5分钟左右

**Personal Story:**
> 帮我把这个经历做成一个短视频，我来提供截图

**Data Visualization:**
> 用 Remotion 做一个展示2024年销售数据的动画视频

## Skill Structure

```
remotion-video/
├── SKILL.md           # Main skill document (workflow + reference)
├── rules/             # Official Remotion rules (30+ files)
│   ├── animations.md
│   ├── timing.md
│   ├── audio.md
│   └── ...
├── scripts/           # TTS generation scripts
│   ├── generate_audio_minimax.py
│   ├── generate_audio_qwen.py
│   ├── generate_audio_edge.py
│   └── check-env.sh
└── templates/
    └── audioConfig.ts
```

## Rules Reference

Key rules files for common tasks:

| Task | Rule File |
|------|-----------|
| Animations | `rules/animations.md`, `rules/timing.md` |
| Video/Audio | `rules/videos.md`, `rules/audio.md` |
| Subtitles | `rules/subtitles.md`, `rules/display-captions.md` |
| 3D Content | `rules/3d.md` |
| Transitions | `rules/transitions.md` |
| Charts | `rules/charts.md` |

## Requirements

- Node.js 18+
- Python 3.8+
- ffmpeg/ffprobe

```bash
# macOS
brew install ffmpeg node

# Ubuntu/Debian
sudo apt install ffmpeg nodejs
```

## Credits

- Official rules from [remotion-dev/skills](https://github.com/remotion-dev/skills)
- Remotion framework by [Remotion](https://remotion.dev)

## License

MIT
