#!/usr/bin/env python3
"""
MiniMax TTS 音频生成脚本（支持断点续作）

特性：
- 检测已存在的音频文件，自动跳过
- 实时显示生成进度
- 生成失败时保留已完成的部分
- 自动更新 Remotion 配置文件

用法：
    python scripts/generate_audio_minimax.py

环境变量：
    MINIMAX_API_KEY: MiniMax API 密钥
    MINIMAX_VOICE_ID: 克隆音色 ID
"""

import os
import requests
import subprocess
from pathlib import Path

# 从环境变量读取配置（推荐）
API_KEY = os.environ.get("MINIMAX_API_KEY")
VOICE_ID = os.environ.get("MINIMAX_VOICE_ID")

if not API_KEY or not VOICE_ID:
    print("❌ 错误: 请设置 MINIMAX_API_KEY 和 MINIMAX_VOICE_ID 环境变量")
    exit(1)

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
    """使用 MiniMax API 生成音频"""
    url = "https://api.minimax.io/v1/t2a_v2"  # 国际版
    # url = "https://api.minimaxi.com/v1/t2a_v2"  # 国内版

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "speech-02-hd",
        "text": scene["text"],
        "stream": False,
        "voice_setting": {"voice_id": VOICE_ID, "speed": 1.0, "vol": 1.0, "pitch": 0},
        "audio_setting": {"sample_rate": 32000, "bitrate": 128000, "format": "mp3", "channel": 1},
    }

    response = requests.post(url, headers=headers, json=payload, timeout=60)
    result = response.json()

    if "data" in result and "audio" in result["data"]:
        audio_data = bytes.fromhex(result["data"]["audio"])
        output_file = OUTPUT_DIR / f"{scene['id']}.mp3"
        output_file.write_bytes(audio_data)

        duration = result.get("extra_info", {}).get("audio_length", 0) / 1000
        if duration == 0:
            duration = get_audio_duration(output_file)

        return {"id": scene["id"], "title": scene["title"], "file": f"{scene['id']}.mp3", "duration": duration, "frames": round(duration * 30)}
    else:
        error = result.get("base_resp", {}).get("status_msg", str(result))
        raise Exception(f"API 错误: {error}")


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"🎙️  MiniMax TTS (Voice: {VOICE_ID[:20]}...)")
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
            results.append({"id": scene["id"], "title": scene["title"], "file": f"{scene['id']}.mp3", "duration": duration, "frames": frames})
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
    """更新 audioConfig.ts - 注意：必须用真正的换行符，不能用字符串 \\n"""
    scenes_lines = []
    for r in results:
        # 使用多行字符串确保正确的换行
        scene_block = f'''  {{
    id: "{r['id']}",
    title: "{r['title']}",
    durationInFrames: {r['frames']},
    audioFile: "{r['file']}",
  }}'''
        scenes_lines.append(scene_block)

    # 用真正的换行符连接，不要用 ",\\n".join()
    scenes_content = ",\n".join(scenes_lines)

    content = f'''// 场景配置（MiniMax TTS 生成）
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
