#!/usr/bin/env python3
"""
Qwen TTS (CosyVoice) 音频生成脚本（支持断点续作）

特性：
- 使用阿里云 DashScope CosyVoice 模型
- 支持多种中文音色，包括声音克隆
- 检测已存在的音频文件，自动跳过
- 实时显示生成进度
- 自动更新 Remotion 配置文件

用法：
    # 推荐：使用公共虚拟环境
    source ~/.claude/envs/remotion-tts/bin/activate && python scripts/generate_audio_qwen.py

    # 或通过 npm script
    npm run audio:qwen

环境变量：
    DASHSCOPE_API_KEY: 阿里云 DashScope API 密钥
    QWEN_VOICE: 音色 ID（可选，默认 longfei）

首次配置公共环境：
    python3 -m venv ~/.claude/envs/remotion-tts
    source ~/.claude/envs/remotion-tts/bin/activate
    pip install requests edge-tts dashscope
"""

import os
import subprocess
from pathlib import Path

try:
    import dashscope
    from dashscope.audio.tts_v2 import SpeechSynthesizer
except ImportError:
    print("❌ 请先安装 dashscope: pip install dashscope")
    exit(1)

# 从环境变量读取配置
API_KEY = os.environ.get("DASHSCOPE_API_KEY")
if not API_KEY:
    print("❌ 错误: 请设置 DASHSCOPE_API_KEY 环境变量")
    print("   获取方式: https://dashscope.console.aliyun.com/apiKey")
    exit(1)

dashscope.api_key = API_KEY

# 音色配置
# 预置音色列表: https://help.aliyun.com/zh/model-studio/developer-reference/cosyvoice-quick-start
# - longxiaochun: 龙小淳（温柔女声）
# - longxiaoxia: 龙小夏（甜美女声）
# - longlaotie: 龙老铁（东北老铁）
# - longshu: 龙叔（成熟男声）
# - longwan: 龙婉（知性女声）
# - longyue: 龙悦（活泼女声）
# - longfei: 龙飞（专业男声，推荐）
# - longjielidou: 龙杰力豆（活力男声）
VOICE = os.environ.get("QWEN_VOICE", "longfei")

# 模型选择
# - cosyvoice-v1: 标准版
# - cosyvoice-v2: 增强版（推荐）
MODEL = "cosyvoice-v2"

# 场景配置 - 每个场景包含 id、title、text
SCENES = [
    {"id": "01-intro", "title": "开场", "text": "欢迎观看本期视频..."},
    {"id": "02-concept", "title": "核心概念", "text": "今天我们来讲..."},
    {"id": "03-demo", "title": "演示", "text": "让我们看一个例子..."},
    {"id": "04-summary", "title": "总结", "text": "感谢观看，下期见！"},
]

OUTPUT_DIR = Path(__file__).parent.parent / "public" / "audio"
CONFIG_FILE = Path(__file__).parent.parent / "src" / "audioConfig.ts"


def get_audio_duration(file_path: Path) -> float:
    """用 ffprobe 获取音频时长"""
    result = subprocess.run(
        ["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(file_path)],
        capture_output=True, text=True,
    )
    return float(result.stdout.strip()) if result.stdout.strip() else 0


def generate_audio(scene: dict) -> dict:
    """使用 DashScope CosyVoice 生成音频"""
    output_file = OUTPUT_DIR / f"{scene['id']}.mp3"

    synthesizer = SpeechSynthesizer(
        model=MODEL,
        voice=VOICE,
        format="mp3",
    )

    # 合成音频
    audio_data = synthesizer.call(scene["text"])

    if audio_data is None:
        raise Exception("音频生成失败，返回为空")

    # 保存文件
    output_file.write_bytes(audio_data)

    # 获取时长
    duration = get_audio_duration(output_file)
    frames = round(duration * 30)  # 30fps

    return {
        "id": scene["id"],
        "title": scene["title"],
        "file": f"{scene['id']}.mp3",
        "duration": duration,
        "frames": frames
    }


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"🎙️  Qwen TTS (Model: {MODEL}, Voice: {VOICE})")
    print(f"📁 输出目录: {OUTPUT_DIR}")
    print("=" * 60)

    results = []
    skipped = 0
    generated = 0

    for i, scene in enumerate(SCENES, 1):
        output_file = OUTPUT_DIR / f"{scene['id']}.mp3"
        prefix = f"[{i}/{len(SCENES)}] {scene['id']}"

        # 断点续作：检查文件是否已存在
        if output_file.exists() and output_file.stat().st_size > 0:
            duration = get_audio_duration(output_file)
            frames = round(duration * 30)
            results.append({
                "id": scene["id"],
                "title": scene["title"],
                "file": f"{scene['id']}.mp3",
                "duration": duration,
                "frames": frames
            })
            print(f"{prefix}: ⏭️  已存在，跳过 ({duration:.2f}s)")
            skipped += 1
            continue

        # 生成新音频
        print(f"{prefix}: 生成中...", end=" ", flush=True)
        try:
            result = generate_audio(scene)
            results.append(result)
            print(f"✅ {result['duration']:.2f}s ({result['frames']} frames)")
            generated += 1
        except Exception as e:
            print(f"❌ {e}")
            print("\n⚠️  生成中断，已完成的音频已保存，可重新运行继续")
            return

    print("=" * 60)
    print(f"✅ 完成: {generated} 新生成, {skipped} 跳过")

    # 更新 audioConfig.ts
    update_config(results)
    print(f"📝 audioConfig.ts 已更新")


def update_config(results):
    """更新 audioConfig.ts"""
    scenes_lines = []
    for r in results:
        scene_block = f'''  {{
    id: "{r['id']}",
    title: "{r['title']}",
    durationInFrames: {r['frames']},
    audioFile: "{r['file']}",
  }}'''
        scenes_lines.append(scene_block)

    scenes_content = ",\n".join(scenes_lines)

    content = f'''// 场景配置（Qwen CosyVoice 生成）
// 自动生成，请勿手动修改

export interface SceneConfig {{
  id: string;
  title: string;
  durationInFrames: number;
  audioFile: string;
}}

export const SCENES: SceneConfig[] = [
{scenes_content},
];

// 计算场景起始帧
export function getSceneStart(sceneIndex: number): number {{
  return SCENES.slice(0, sceneIndex).reduce((sum, s) => sum + s.durationInFrames, 0);
}}

// 总帧数（加上片头片尾缓冲）
export const TOTAL_FRAMES = SCENES.reduce((sum, s) => sum + s.durationInFrames, 0) + 60;

// 帧率
export const FPS = 30;
'''
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(content)


if __name__ == "__main__":
    main()
