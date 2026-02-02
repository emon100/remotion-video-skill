#!/bin/bash
# Remotion 视频渲染环境检查脚本
# 用法: bash scripts/check-env.sh

echo "🔍 检查 Remotion 渲染环境..."
echo "================================"

# 检查 Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js 未安装"
    echo "   安装方式: brew install node"
    exit 1
fi
echo "✅ Node.js: $(node -v)"

# 检查 npm
if ! command -v npm &> /dev/null; then
    echo "❌ npm 未安装"
    exit 1
fi
echo "✅ npm: $(npm -v)"

# 检查 ffmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo "❌ ffmpeg 未安装"
    echo "   安装方式: brew install ffmpeg"
    exit 1
fi
echo "✅ ffmpeg: $(ffmpeg -version 2>&1 | head -1)"

# 检查 ffprobe
if ! command -v ffprobe &> /dev/null; then
    echo "❌ ffprobe 未安装（通常与 ffmpeg 一起安装）"
    exit 1
fi
echo "✅ ffprobe: 已安装"

# 检查 Python 公共虚拟环境
VENV_PATH=~/.claude/envs/remotion-tts
if [ -d "$VENV_PATH" ]; then
    echo "✅ Python 虚拟环境: $VENV_PATH"

    # 检查关键依赖
    source "$VENV_PATH/bin/activate"

    if python -c "import requests" 2>/dev/null; then
        echo "   ✅ requests 已安装"
    else
        echo "   ⚠️  requests 未安装，运行: pip install requests"
    fi

    if python -c "import edge_tts" 2>/dev/null; then
        echo "   ✅ edge-tts 已安装"
    else
        echo "   ⚠️  edge-tts 未安装，运行: pip install edge-tts"
    fi

    if python -c "import dashscope" 2>/dev/null; then
        echo "   ✅ dashscope 已安装"
    else
        echo "   ⚠️  dashscope 未安装，运行: pip install dashscope"
    fi

    deactivate 2>/dev/null
else
    echo "⚠️  Python 虚拟环境未配置"
    echo "   创建方式:"
    echo "   python3 -m venv ~/.claude/envs/remotion-tts"
    echo "   source ~/.claude/envs/remotion-tts/bin/activate"
    echo "   pip install requests edge-tts dashscope"
fi

# 检查 Chrome Headless Shell 缓存
CHROME_CACHE=~/.cache/remotion
if [ -d "$CHROME_CACHE" ] && [ "$(ls -A $CHROME_CACHE 2>/dev/null)" ]; then
    echo "✅ Chrome Headless Shell: 已缓存于 $CHROME_CACHE"
    ls -la "$CHROME_CACHE" 2>/dev/null | head -5
else
    echo "⚠️  Chrome Headless Shell 未缓存"
    echo "   首次渲染时会自动下载（约 150MB）"
    echo "   或手动指定系统 Chrome:"
    echo "   export PUPPETEER_EXECUTABLE_PATH='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'"
fi

# 检查系统 Chrome
if [ -f "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" ]; then
    echo "✅ 系统 Chrome: 已安装"
else
    echo "ℹ️  系统 Chrome: 未安装（可选）"
fi

echo ""
echo "================================"
echo "✅ 环境检查完成"
echo ""
echo "💡 快速开始:"
echo "   npm run dev        # 启动预览"
echo "   npm run audio:edge # 生成语音（免费）"
echo "   npm run render     # 渲染视频"
