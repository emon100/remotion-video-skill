# remotion-video

[English](README.md)

Claude Code Skill - 使用 Remotion 框架编程式创建视频。整合官方最佳实践、中文 TTS 支持和结构化视频创作工作流。

## 特性

- **纯 Node.js/TypeScript** - 无需 Python
- **自动重试** - TTS 失败自动重试（默认 3 次）
- **多 TTS 提供商** - MiniMax（音色克隆）、Qwen（中文）、Edge TTS（免费）
- **官方规则集成** - 30+ 规则文件来自 [remotion-dev/skills](https://github.com/remotion-dev/skills)

## 安装

### Claude Code 用户

```bash
git clone https://github.com/emon100/remotion-video-skill.git
cp -r remotion-video-skill ~/.claude/skills/remotion-video
```

然后重启 Claude Code 或开启新会话。

### 系统依赖

```bash
# macOS
brew install node ffmpeg

# Ubuntu/Debian
sudo apt install nodejs ffmpeg
```

### TTS 配置（选择一种）

| 方案 | 配置 | 优点 | 价格 |
|------|------|------|------|
| **Edge TTS** | `npm install msedge-tts` | 免费，开箱即用 | 免费 |
| **Qwen TTS** | `DASHSCOPE_API_KEY` | 中文音质优秀 | ¥0.02/千字 |
| **MiniMax** | `MINIMAX_API_KEY` + `MINIMAX_VOICE_ID` | 支持音色克隆 | ¥0.05/千字 |

## 使用方法

触发词：

- "用代码做视频" / "编程视频"
- "Remotion" / "remotion"
- "/remotion-video"

### TTS 语音生成

```bash
# 自动选择可用提供商
npx ts-node scripts/generate-audio.ts

# 指定提供商
npx ts-node scripts/generate-audio.ts --provider edge

# 设置重试次数
npx ts-node scripts/generate-audio.ts --retries 5
```

### 示例提示词

**教程视频：**
> 帮我做一个讲解 CNN 卷积神经网络的教程视频，5分钟左右

**个人故事：**
> 帮我把这个经历做成一个短视频，我来提供截图

## Skill 结构

```
remotion-video/
├── SKILL.md              # 主技能文档
├── rules/                # 官方 Remotion 规则（30+ 文件）
├── scripts/
│   ├── generate-audio.ts # TTS 生成脚本（TypeScript）
│   └── check-env.sh      # 环境检查
└── templates/
    └── audioConfig.ts
```

## 系统要求

- Node.js 18+
- ffmpeg/ffprobe

## 致谢

- 官方规则来自 [remotion-dev/skills](https://github.com/remotion-dev/skills)
- Remotion 框架 by [Remotion](https://remotion.dev)

## 许可证

MIT
