#!/usr/bin/env npx ts-node
/**
 * TTS 音频生成脚本 (TypeScript, 纯 Node.js)
 *
 * 特性：
 * - 支持多种 TTS 提供商（MiniMax、Qwen、Edge TTS）
 * - 自动重试失败项目（默认 3 次）
 * - 自动更新 audioConfig.ts
 *
 * 用法：
 *   npx ts-node scripts/generate-audio.ts              # 使用默认提供商
 *   npx ts-node scripts/generate-audio.ts --provider edge
 *   npx ts-node scripts/generate-audio.ts --retries 5  # 设置重试次数
 *
 * 环境变量：
 *   MINIMAX_API_KEY, MINIMAX_VOICE_ID  - MiniMax TTS
 *   DASHSCOPE_API_KEY, QWEN_VOICE      - Qwen TTS
 *   EDGE_VOICE                         - Edge TTS 音色
 */

import * as fs from "fs";
import * as path from "path";
import { execSync } from "child_process";

// ============== 类型定义 ==============

interface Scene {
  id: string;
  title: string;
  text: string;
}

interface GeneratedScene extends Scene {
  file: string;
  duration: number;
  frames: number;
}

interface TTSProvider {
  name: string;
  generate(text: string, outputPath: string): Promise<void>;
  checkConfig(): string | null;
}

// ============== 配置 ==============

const FPS = 30;
const DEFAULT_RETRIES = 3;
const RETRY_DELAY_MS = 1000;

const PROJECT_ROOT = path.resolve(__dirname, "..");
const AUDIO_DIR = path.join(PROJECT_ROOT, "public", "audio");
const CONFIG_FILE = path.join(PROJECT_ROOT, "src", "audioConfig.ts");

// 场景配置 - 实际项目中会被覆盖
let SCENES: Scene[] = [
  { id: "01-intro", title: "开场", text: "欢迎观看本期视频..." },
  { id: "02-main", title: "主要内容", text: "今天我们来讲..." },
  { id: "03-outro", title: "结尾", text: "感谢观看，下期见！" },
];

// ============== 工具函数 ==============

function getAudioDuration(filePath: string): number {
  try {
    const result = execSync(
      `ffprobe -v quiet -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "${filePath}"`,
      { encoding: "utf-8" }
    );
    return parseFloat(result.trim()) || 0;
  } catch {
    return 0;
  }
}

function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function retry<T>(
  fn: () => Promise<T>,
  maxRetries: number,
  delayMs: number,
  onRetry?: (attempt: number, error: Error) => void
): Promise<T> {
  let lastError: Error = new Error("Unknown error");

  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error instanceof Error ? error : new Error(String(error));

      if (attempt < maxRetries) {
        onRetry?.(attempt, lastError);
        await sleep(delayMs * attempt); // 指数退避
      }
    }
  }

  throw lastError;
}

// ============== TTS 提供商实现 ==============

const minimaxProvider: TTSProvider = {
  name: "minimax",

  checkConfig() {
    if (!process.env.MINIMAX_API_KEY) return "缺少 MINIMAX_API_KEY";
    if (!process.env.MINIMAX_VOICE_ID) return "缺少 MINIMAX_VOICE_ID";
    return null;
  },

  async generate(text: string, outputPath: string) {
    const response = await fetch("https://api.minimax.io/v1/t2a_v2", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${process.env.MINIMAX_API_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        model: "speech-02-hd",
        text,
        stream: false,
        voice_setting: {
          voice_id: process.env.MINIMAX_VOICE_ID,
          speed: 1.0,
          vol: 1.0,
          pitch: 0,
        },
        audio_setting: {
          sample_rate: 32000,
          bitrate: 128000,
          format: "mp3",
          channel: 1,
        },
      }),
    });

    const result = await response.json();

    if (result.data?.audio) {
      fs.writeFileSync(outputPath, Buffer.from(result.data.audio, "hex"));
    } else {
      throw new Error(result.base_resp?.status_msg || JSON.stringify(result));
    }
  },
};

const qwenProvider: TTSProvider = {
  name: "qwen",

  checkConfig() {
    if (!process.env.DASHSCOPE_API_KEY) return "缺少 DASHSCOPE_API_KEY";
    return null;
  },

  async generate(text: string, outputPath: string) {
    const voice = process.env.QWEN_VOICE || "longfei";

    const response = await fetch(
      "https://dashscope.aliyuncs.com/api/v1/services/aigc/text2audio/generate",
      {
        method: "POST",
        headers: {
          Authorization: `Bearer ${process.env.DASHSCOPE_API_KEY}`,
          "Content-Type": "application/json",
          "X-DashScope-Async": "disable",
        },
        body: JSON.stringify({
          model: "cosyvoice-v2",
          input: { text },
          parameters: { voice },
        }),
      }
    );

    const result = await response.json();

    if (result.output?.audio) {
      fs.writeFileSync(outputPath, Buffer.from(result.output.audio, "base64"));
    } else if (result.output?.audio_url) {
      const audioRes = await fetch(result.output.audio_url);
      fs.writeFileSync(outputPath, Buffer.from(await audioRes.arrayBuffer()));
    } else {
      throw new Error(result.message || JSON.stringify(result));
    }
  },
};

const edgeProvider: TTSProvider = {
  name: "edge",

  checkConfig() {
    return null;
  },

  async generate(text: string, outputPath: string) {
    const voice = process.env.EDGE_VOICE || "zh-CN-YunyangNeural";

    // 方案 1: msedge-tts npm 包
    try {
      const { MsEdgeTTS } = await import("msedge-tts");
      const tts = new MsEdgeTTS();
      await tts.setMetadata(voice, "audio-24khz-96kbitrate-mono-mp3");
      const readable = tts.toStream(text);

      const chunks: Buffer[] = [];
      for await (const chunk of readable) {
        chunks.push(Buffer.from(chunk));
      }
      fs.writeFileSync(outputPath, Buffer.concat(chunks));
      return;
    } catch {
      // 包未安装
    }

    // 方案 2: 使用在线 API（备选）
    throw new Error("请安装 msedge-tts: npm install msedge-tts");
  },
};

// ============== 提供商选择 ==============

const providers: Record<string, TTSProvider> = {
  minimax: minimaxProvider,
  qwen: qwenProvider,
  edge: edgeProvider,
};

function selectProvider(): TTSProvider {
  for (const name of ["minimax", "qwen", "edge"]) {
    if (!providers[name].checkConfig()) return providers[name];
  }
  return providers.edge;
}

// ============== 主逻辑 ==============

async function generateAudio(options: { provider?: string; retries?: number }) {
  const maxRetries = options.retries || DEFAULT_RETRIES;

  // 选择提供商
  let provider: TTSProvider;
  if (options.provider) {
    provider = providers[options.provider];
    if (!provider) {
      console.error(`❌ 未知提供商: ${options.provider}`);
      console.log(`可用: ${Object.keys(providers).join(", ")}`);
      process.exit(1);
    }
    const error = provider.checkConfig();
    if (error) {
      console.error(`❌ ${error}`);
      process.exit(1);
    }
  } else {
    provider = selectProvider();
  }

  console.log(`🎙️  TTS: ${provider.name} (重试: ${maxRetries}次)`);
  console.log(`📁 输出: ${AUDIO_DIR}`);
  console.log("=".repeat(50));

  // 确保目录存在
  fs.mkdirSync(AUDIO_DIR, { recursive: true });

  const results: GeneratedScene[] = [];
  let failed = 0;

  for (let i = 0; i < SCENES.length; i++) {
    const scene = SCENES[i];
    const outputPath = path.join(AUDIO_DIR, `${scene.id}.mp3`);
    const prefix = `[${i + 1}/${SCENES.length}] ${scene.id}`;

    process.stdout.write(`${prefix}: 生成中`);

    try {
      await retry(
        () => provider.generate(scene.text, outputPath),
        maxRetries,
        RETRY_DELAY_MS,
        (attempt) => process.stdout.write(` (重试${attempt})`)
      );

      const duration = getAudioDuration(outputPath);
      const frames = Math.round(duration * FPS);

      results.push({ ...scene, file: `${scene.id}.mp3`, duration, frames });
      console.log(` ✅ ${duration.toFixed(2)}s`);
    } catch (error) {
      console.log(` ❌ 失败`);
      console.log(`   ${error instanceof Error ? error.message : error}`);
      failed++;
    }
  }

  console.log("=".repeat(50));
  console.log(`✅ 成功: ${results.length}, ❌ 失败: ${failed}`);

  if (results.length > 0) {
    updateAudioConfig(results, provider.name);
    console.log(`📝 已更新 audioConfig.ts`);
  }

  if (failed > 0) {
    process.exit(1);
  }
}

function updateAudioConfig(scenes: GeneratedScene[], providerName: string) {
  const content = `// 场景配置（自动生成）
// 生成时间: ${new Date().toISOString()}
// TTS: ${providerName}

export interface SceneConfig {
  id: string;
  title: string;
  text: string;
  durationInFrames: number;
  audioFile: string;
}

export const SCENES: SceneConfig[] = [
${scenes
  .map(
    (s) => `  {
    id: "${s.id}",
    title: "${s.title}",
    text: \`${s.text.replace(/`/g, "\\`")}\`,
    durationInFrames: ${s.frames},
    audioFile: "${s.file}",
  }`
  )
  .join(",\n")}
];

export function getSceneStart(index: number): number {
  return SCENES.slice(0, index).reduce((sum, s) => sum + s.durationInFrames, 0);
}

export const TOTAL_FRAMES = SCENES.reduce((sum, s) => sum + s.durationInFrames, 0) + 60;
export const FPS = ${FPS};
`;

  fs.mkdirSync(path.dirname(CONFIG_FILE), { recursive: true });
  fs.writeFileSync(CONFIG_FILE, content);
}

// ============== CLI ==============

function parseArgs() {
  const args = process.argv.slice(2);
  const opts: { provider?: string; retries?: number; help?: boolean } = {};

  for (let i = 0; i < args.length; i++) {
    if (args[i] === "-p" || args[i] === "--provider") opts.provider = args[++i];
    else if (args[i] === "-r" || args[i] === "--retries")
      opts.retries = parseInt(args[++i]);
    else if (args[i] === "-h" || args[i] === "--help") opts.help = true;
  }
  return opts;
}

const opts = parseArgs();

if (opts.help) {
  console.log(`
用法: npx ts-node scripts/generate-audio.ts [选项]

选项:
  -p, --provider <name>  TTS 提供商 (minimax, qwen, edge)
  -r, --retries <n>      重试次数 (默认: 3)
  -h, --help             帮助

环境变量:
  MINIMAX_API_KEY, MINIMAX_VOICE_ID  - MiniMax
  DASHSCOPE_API_KEY, QWEN_VOICE      - Qwen
  EDGE_VOICE                         - Edge TTS
`);
  process.exit(0);
}

generateAudio(opts).catch((e) => {
  console.error("❌", e.message);
  process.exit(1);
});
