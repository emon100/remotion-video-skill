# TTS 提供商配置详情

## MiniMax TTS（音色克隆）

1. 注册 https://www.minimax.io（国际版）或 https://platform.minimaxi.com（国内版）
2. 获取 API Key 和 Voice ID

```bash
export MINIMAX_API_KEY="your_api_key"
export MINIMAX_VOICE_ID="your_voice_id"
```

**API 域名**：国际版 `api.minimax.io`，国内版 `api.minimaxi.com`

**价格**：¥0.05-0.1/千字符

---

## Qwen TTS (CosyVoice)

1. 注册阿里云 DashScope：https://dashscope.console.aliyun.com/
2. 获取 API Key

```bash
export DASHSCOPE_API_KEY="your_api_key"
export QWEN_VOICE="longfei"  # 可选
```

**可用音色**：

| 音色 ID | 名称 | 风格 |
|---------|------|------|
| longfei | 龙飞 | 专业男声（推荐） |
| longshu | 龙叔 | 成熟男声 |
| longwan | 龙婉 | 知性女声 |
| longxiaochun | 龙小淳 | 温柔女声 |

**价格**：¥0.02-0.04/千字符

---

## Edge TTS（免费）

无需 API Key，安装 npm 包即可。

```bash
npm install msedge-tts
```

| 语音 ID | 名称 | 风格 |
|---------|------|------|
| zh-CN-YunyangNeural | 云扬 | 专业播音腔（推荐） |
| zh-CN-XiaoxiaoNeural | 晓晓 | 温暖自然 |
| zh-CN-YunxiNeural | 云希 | 阳光少年 |

设置音色：`export EDGE_VOICE="zh-CN-YunyangNeural"`

---

## 火山引擎 Seed-TTS（中文多角色首选）

字节跳动旗下，音质最佳，200+ 预置音色。

1. 注册 https://console.volcengine.com/ → 开通语音合成服务
2. 创建应用获取 App ID 和 Access Token

**API 端点**：`https://openspeech.bytedance.com/api/v3/tts/unidirectional`

### ⚠️ 关键踩坑点

1. **音色与 resource_id 必须匹配**（不匹配返回空音频，无报错！）：
   - `uranus` 系列 → `seed-tts-2.0`
   - `moon` 系列 → `seed-tts-1.0`
2. **响应格式是流式 JSON Lines**：音频在 `data` 字段（不是 `audio`）
3. **成功码有两个**：`0` 和 `20000000` 都表示成功

### 多角色配置

```python
VOLCANO_CONFIG = {
    "app_id": "your_app_id",
    "access_token": "your_access_token",
    "api_url": "https://openspeech.bytedance.com/api/v3/tts/unidirectional",
}

ROLE_CONFIG = {
    "user": {
        "voice": "zh_male_m191_uranus_bigtts",
        "resource_id": "seed-tts-2.0",
    },
    "ai": {
        "voice": "zh_male_jieshuoxiaoming_moon_bigtts",
        "resource_id": "seed-tts-1.0",
    },
}
```

### 请求与响应

```python
headers = {
    "X-Api-App-Id": config["app_id"],
    "X-Api-Access-Key": config["access_token"],
    "X-Api-Resource-Id": role["resource_id"],
    "Content-Type": "application/json",
}

payload = {
    "user": {"uid": "video-project"},
    "req_params": {
        "text": "要合成的文本",
        "speaker": role["voice"],
        "audio_params": {"format": "mp3", "sample_rate": 24000},
    },
}

# 流式响应解析
resp = requests.post(api_url, headers=headers, json=payload, stream=True, timeout=60)
audio_chunks = []
for line in resp.iter_lines():
    if not line:
        continue
    data = json.loads(line)
    code = data.get("code", data.get("status_code", 0))
    if code not in (0, 20000000):
        raise RuntimeError(f"API error {code}: {data.get('message', 'unknown')}")
    audio_b64 = data.get("data") or data.get("audio")
    if audio_b64:
        audio_chunks.append(base64.b64decode(audio_b64))
```

### 推荐中文音色

| 音色 ID | 系列 | resource_id | 风格 |
|---------|------|-------------|------|
| zh_male_m191_uranus_bigtts | uranus | seed-tts-2.0 | 自然男声 |
| zh_male_jieshuoxiaoming_moon_bigtts | moon | seed-tts-1.0 | 解说男声 |
| zh_female_wanwanxiaohe_moon_bigtts | moon | seed-tts-1.0 | 温柔女声 |

---

## Remotion 音频同步

```tsx
import { Audio, Sequence, staticFile } from "remotion";
import { SCENES, getSceneStart } from "./audioConfig";

// 每个场景一个 Sequence，音频自动同步
{SCENES.map((scene, idx) => (
  <Sequence key={scene.id} from={getSceneStart(idx)} durationInFrames={scene.durationInFrames}>
    <SceneComponent />
    <Audio src={staticFile(`audio/${scene.audioFile}`)} />
  </Sequence>
))}
```

## 音频后处理（ffmpeg）

### 去除首尾静音 + 加速

```bash
# 去除首尾静音 + 1.2x 加速
ffmpeg -y -i input.mp3 \
  -af "silenceremove=start_periods=1:start_threshold=-40dB:start_duration=0.05,\
areverse,silenceremove=start_periods=1:start_threshold=-40dB:start_duration=0.05,\
areverse,atempo=1.2" \
  -b:a 192k output.mp3
```

原理：`silenceremove` 去头 → `areverse` + `silenceremove` 去尾 → `areverse` 翻回 → `atempo` 加速

### 批量处理

```bash
for f in public/audio/*.mp3; do
  tmp="${f%.mp3}_tmp.mp3"
  ffmpeg -y -i "$f" \
    -af "silenceremove=start_periods=1:start_threshold=-40dB:start_duration=0.05,\
areverse,silenceremove=start_periods=1:start_threshold=-40dB:start_duration=0.05,\
areverse,atempo=1.2" \
    -b:a 192k "$tmp" && mv "$tmp" "$f"
done
```

### 片头音乐渐弱淡出

```bash
# 8s 片头，前 5s 正常，后 3s 淡出
ffmpeg -y -i music.mp3 -af "afade=t=out:st=5:d=3" -t 8 -b:a 192k output.mp3
```

### ffprobe 获取时长并更新配置

```python
import subprocess, math

def get_audio_duration(file_path):
    result = subprocess.run(
        ['ffprobe', '-v', 'quiet', '-show_entries', 'format=duration',
         '-of', 'csv=p=0', str(file_path)],
        capture_output=True, text=True
    )
    return float(result.stdout.strip())

# 向上取整 + 1s 缓冲
rounded = math.ceil(get_audio_duration("audio.mp3")) + 1
```
