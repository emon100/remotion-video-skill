# 教程类视频架构（场景驱动）

核心思想：**音频驱动场景切换**。

```
音频脚本 → TTS 生成 → audioConfig.ts → 场景组件 → 视频渲染
```

1. **音频决定时长**：每个场景的持续时间由音频长度决定
2. **场景即章节**：一个概念 = 一个场景 = 一段音频
3. **配置即真理**：`audioConfig.ts` 是音画同步的单一数据源

## audioConfig.ts 模板

参见 `templates/audioConfig.ts`，包含 SceneConfig 接口、SCENES 数组、getSceneStart()、TOTAL_FRAMES。

## 场景切换 Hook

```tsx
import { useCurrentFrame } from "remotion";
import { SCENES } from "./audioConfig";

const useCurrentSceneIndex = () => {
  const frame = useCurrentFrame();
  let accumulated = 0;
  for (let i = 0; i < SCENES.length; i++) {
    accumulated += SCENES[i].durationInFrames;
    if (frame < accumulated) return i;
  }
  return SCENES.length - 1;
};
```

## 主场景组件模式

```tsx
export const TutorialVideo: React.FC = () => {
  const { width, height } = useVideoConfig();
  const sceneIndex = useCurrentSceneIndex();
  const currentScene = SCENES[sceneIndex];

  return (
    <AbsoluteFill>
      {/* 场景内容：根据 sceneIndex 条件渲染 */}
      <ThreeCanvas width={width} height={height}>
        {sceneIndex === 0 && <Scene01Intro />}
        {sceneIndex === 1 && <Scene02Concept />}
      </ThreeCanvas>

      {/* 音频同步 */}
      {SCENES.map((scene, idx) => (
        <Sequence key={scene.id} from={getSceneStart(idx)} durationInFrames={scene.durationInFrames}>
          <Audio src={staticFile(`audio/${scene.audioFile}`)} />
        </Sequence>
      ))}

      {/* UI 层：标题 + 进度条 */}
    </AbsoluteFill>
  );
};
```

## Root.tsx

```tsx
<Composition
  id="Tutorial"
  component={TutorialVideo}
  fps={30}
  durationInFrames={TOTAL_FRAMES}  // 从 audioConfig 动态获取
  width={1920}
  height={1080}
/>
```

## 踩坑经验

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 场景切换生硬 | 直接切换无过渡 | 用 spring/interpolate 添加入场动画 |
| 3D 内容与音频不同步 | 硬编码帧数 | 所有时长从 audioConfig 读取 |
| 渲染时 WebGL 崩溃 | 多个 ThreeCanvas 同时存在 | 用 sceneIndex 条件渲染 |
| 视频太简略 | 只有一个大场景 | 一个概念 = 一个场景组件 |

## 场景组件设计原则

1. **单一职责**：每个场景只负责一个概念
2. **独立动画**：Sequence 内 useCurrentFrame() 从 0 开始
3. **延迟出现**：用 delay 参数控制元素依次出现

```tsx
const Scene02Input: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const gridScale = spring({ frame, fps, config: { damping: 15 } });
  return <group><PixelGrid scale={gridScale * 1.5} /></group>;
};
```

## 相机控制器

```tsx
// ✅ 直接设置位置，不用插值（避免持续抖动）
const CameraController: React.FC<{ sceneIndex: number }> = ({ sceneIndex }) => {
  const { camera } = useThree();
  const settings: Record<number, [number, number, number]> = {
    0: [0, 0, 4], 1: [0, 0, 3], 2: [-0.5, 0, 3.5],
  };
  const target = settings[sceneIndex] || [0, 0, 4];
  camera.position.set(...target);
  camera.lookAt(0, 0, 0);
  return null;
};
```

⚠️ 不要用 `position += (target - position) * factor`，永远无法精确收敛，导致画面持续抖动。
