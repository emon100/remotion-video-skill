#!/bin/bash
# Remotion 视频渲染环境检查脚本
# 用法: bash scripts/check-env.sh

echo "🔍 检查 Remotion 渲染环境..."
echo "================================"

# 检查 Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js 未安装"
    echo "   安装: brew install node"
    exit 1
fi
echo "✅ Node.js: $(node -v)"

# 检查 npm
if ! command -v npm &> /dev/null; then
    echo "❌ npm 未安装"
    exit 1
fi
echo "✅ npm: $(npm -v)"

# 检查 npx
if ! command -v npx &> /dev/null; then
    echo "❌ npx 未安装"
    exit 1
fi
echo "✅ npx: 已安装"

# 检查 ffmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo "❌ ffmpeg 未安装"
    echo "   安装: brew install ffmpeg"
    exit 1
fi
echo "✅ ffmpeg: $(ffmpeg -version 2>&1 | head -1)"

# 检查 ffprobe
if ! command -v ffprobe &> /dev/null; then
    echo "❌ ffprobe 未安装"
    exit 1
fi
echo "✅ ffprobe: 已安装"

# 检查 Chrome Headless Shell 缓存
CHROME_CACHE=~/.cache/remotion
if [ -d "$CHROME_CACHE" ] && [ "$(ls -A $CHROME_CACHE 2>/dev/null)" ]; then
    echo "✅ Chrome Headless Shell: 已缓存"
else
    echo "⚠️  Chrome Headless Shell: 未缓存（首次渲染会自动下载）"
fi

# 检查系统 Chrome
if [ -f "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" ]; then
    echo "✅ 系统 Chrome: 已安装"
fi

# 检查 TTS 依赖
echo ""
echo "📦 TTS 依赖检查..."

# 检查 msedge-tts（Edge TTS 需要）
if npm list msedge-tts &>/dev/null 2>&1; then
    echo "✅ msedge-tts: 已安装"
else
    echo "⚠️  msedge-tts: 未安装 (Edge TTS 需要)"
    echo "   安装: npm install msedge-tts"
fi

# 检查环境变量
echo ""
echo "🔑 API 配置检查..."
if [ -n "$MINIMAX_API_KEY" ] && [ -n "$MINIMAX_VOICE_ID" ]; then
    echo "✅ MiniMax TTS: 已配置"
elif [ -n "$DASHSCOPE_API_KEY" ]; then
    echo "✅ Qwen TTS: 已配置"
else
    echo "ℹ️  无付费 TTS 配置，将使用 Edge TTS（免费）"
fi

echo ""
echo "================================"
echo "✅ 环境检查完成"
echo ""
echo "💡 快速开始:"
echo "   npm run dev           # 启动预览"
echo "   npm run audio         # 生成语音"
echo "   npm run render        # 渲染视频"
