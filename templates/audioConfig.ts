// 场景配置（TTS 生成后自动更新）
export interface SceneConfig {
  id: string;
  title: string;
  durationInFrames: number;
  audioFile: string;
}

export const SCENES: SceneConfig[] = [
  { id: "01-intro", title: "开场", durationInFrames: 300, audioFile: "01-intro.mp3" },
  { id: "02-concept", title: "核心概念", durationInFrames: 450, audioFile: "02-concept.mp3" },
  { id: "03-demo", title: "演示", durationInFrames: 600, audioFile: "03-demo.mp3" },
  // ... 更多场景
];

// 计算场景起始帧
export function getSceneStart(sceneIndex: number): number {
  return SCENES.slice(0, sceneIndex).reduce((sum, s) => sum + s.durationInFrames, 0);
}

// 总帧数（可加片头片尾缓冲）
export const TOTAL_FRAMES = SCENES.reduce((sum, s) => sum + s.durationInFrames, 0) + 60;

// 帧率
export const FPS = 30;
