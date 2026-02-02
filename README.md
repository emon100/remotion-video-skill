# remotion-video

[中文文档](README_CN.md)

A Claude Code Skill for creating programmatic videos with Remotion framework. This skill integrates official Remotion best practices with enhanced Chinese TTS support and a structured video creation workflow.

## Features

- **Pure Node.js/TypeScript** - No Python required
- **Auto-Retry TTS** - Automatic retry on failure (default 3 times)
- **Multiple TTS Providers** - MiniMax (voice cloning), Qwen (Chinese), Edge TTS (free)
- **Official Rules Integration** - 30+ rules from [remotion-dev/skills](https://github.com/remotion-dev/skills)

## Installation

### For Claude Code Users

```bash
git clone https://github.com/emon100/remotion-video-skill.git
cp -r remotion-video-skill ~/.claude/skills/remotion-video
```

Then restart Claude Code or start a new session.

### System Dependencies

```bash
# macOS
brew install node ffmpeg

# Ubuntu/Debian
sudo apt install nodejs ffmpeg
```

### TTS Setup (Choose One)

| Provider | Setup | Pros | Pricing |
|----------|-------|------|---------|
| **Edge TTS** | `npm install msedge-tts` | Free, no API key | Free |
| **Qwen TTS** | `DASHSCOPE_API_KEY` | Excellent Chinese | ¥0.02/1k chars |
| **MiniMax** | `MINIMAX_API_KEY` + `MINIMAX_VOICE_ID` | Voice cloning | ¥0.05/1k chars |

## Usage

Trigger the skill with:

- "用代码做视频" / "编程视频"
- "Remotion" / "remotion"
- "/remotion-video"

### TTS Generation

```bash
# Auto-select available provider
npx ts-node scripts/generate-audio.ts

# Specify provider
npx ts-node scripts/generate-audio.ts --provider edge

# Set retry count
npx ts-node scripts/generate-audio.ts --retries 5
```

### Example Prompts

**Tutorial Video:**
> 帮我做一个讲解 CNN 卷积神经网络的教程视频，5分钟左右

**Personal Story:**
> 帮我把这个经历做成一个短视频，我来提供截图

## Skill Structure

```
remotion-video/
├── SKILL.md              # Main skill document
├── rules/                # Official Remotion rules (30+ files)
├── scripts/
│   ├── generate-audio.ts # TTS generation (TypeScript)
│   └── check-env.sh      # Environment check
└── templates/
    └── audioConfig.ts
```

## Requirements

- Node.js 18+
- ffmpeg/ffprobe

## Credits

- Official rules from [remotion-dev/skills](https://github.com/remotion-dev/skills)
- Remotion framework by [Remotion](https://remotion.dev)

## License

MIT
