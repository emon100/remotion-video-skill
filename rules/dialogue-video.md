# 对话式视频架构

与教程视频「教师→学生」不同，对话式视频有两个角色来回对话，需要多层分工。

## audioConfig.ts 扩展

```typescript
export interface SceneConfig {
  id: string;
  speaker: "user" | "ai" | "system";
  text: string;
  durationInSeconds: number;
  durationInFrames?: number;
  audioFile?: string;
  sceneType:
    | "brand-intro"   // 片头
    | "dialogue"      // 对话场景
    | "terminal"      // 终端展示
    | "animation"     // 动画演示
    | "realfootage"   // 真实素材
    | "ending";       // 结尾
  visualHint?: string; // 画面提示（给开发者看）
}
```

## 多层视频架构

```
┌──────────────────────────────────────┐
│  Layer 6: 进度条                      │  ProgressBar
├──────────────────────────────────────┤
│  Layer 5: 音频播放                    │  <Audio> in <Sequence>
├──────────────────────────────────────┤
│  Layer 4: 术语解释浮窗                │  TermGlossaryLayer
├──────────────────────────────────────┤
│  Layer 3: 全局 UI（状态栏等）          │  SSH StatusBar
├──────────────────────────────────────┤
│  Layer 2: 对话气泡/字幕               │  ChatOverlay / SubtitleBar
├──────────────────────────────────────┤
│  Layer 1: 场景主画面                  │  根据 sceneType 条件渲染
├──────────────────────────────────────┤
│  Layer 0: 背景                       │  GradientBg + GridBg
└──────────────────────────────────────┘
```

每层通过 `position: absolute` 叠加，`useCurrentSceneIndex()` 控制内容。

## ChatOverlay 组件

根据 speaker 切换气泡方向、颜色、头像：

```tsx
const ChatOverlay: React.FC<{ speaker: "user" | "ai"; text: string }> = ({ speaker, text }) => {
  const isUser = speaker === "user";
  return (
    <div style={{
      position: "absolute", bottom: 60,
      left: isUser ? "auto" : 50, right: isUser ? 50 : "auto",
      flexDirection: isUser ? "row-reverse" : "row",
    }}>
      <div>{isUser ? <AvatarUser /> : <AvatarAI />}</div>
      <div style={{
        borderRadius: isUser ? "24px 24px 6px 24px" : "24px 24px 24px 6px",
        backgroundColor: isUser ? "#dbeafe" : "#ccfbf1",
      }}>
        {text}
      </div>
    </div>
  );
};
```

## SubtitleBar 组件（结尾字幕）

结尾场景使用居中半透明字幕条代替对话气泡：

```tsx
const SubtitleBar: React.FC<{ text: string }> = ({ text }) => (
  <div style={{
    position: "absolute", bottom: 60, left: "50%",
    transform: "translateX(-50%)",
    padding: "16px 40px", borderRadius: 12,
    backgroundColor: "rgba(0,0,0,0.6)", backdropFilter: "blur(8px)",
  }}>
    <div style={{ fontSize: 32, color: "#fff", textAlign: "center" }}>{text}</div>
  </div>
);
```

## 术语解释浮窗（TermGlossary）

为非技术观众解释专业术语，通知样式弹窗。

### 数据结构

```tsx
interface TermEntry {
  term: string;
  explanation: string;
  sceneId: string;      // 在哪个场景出现
  delayFrames: number;  // 场景内延迟帧数
}

const TOOLTIP_DURATION = 150; // 5s at 30fps

const GLOSSARY_TERMS: TermEntry[] = [
  { term: "kernel panic", explanation: '内核崩溃，相当于 Linux 版"蓝屏"', sceneId: "hook", delayFrames: 75 },
  { term: "apt", explanation: "Ubuntu 的软件包管理器，类似应用商店", sceneId: "backstory", delayFrames: 200 },
  // ...
];
```

### 调度逻辑

用 `useMemo` 预计算绝对帧范围，避免每帧重算：

```tsx
const TermGlossaryLayer: React.FC = () => {
  const frame = useCurrentFrame();
  const scheduled = React.useMemo(() => {
    const sceneMap: Record<string, number> = {};
    SCENES.forEach((s, i) => { sceneMap[s.id] = i; });
    return GLOSSARY_TERMS.map((t) => {
      const idx = sceneMap[t.sceneId];
      if (idx === undefined) return null;
      const start = getSceneStart(idx) + t.delayFrames;
      return { ...t, startFrame: start, endFrame: start + TOOLTIP_DURATION };
    }).filter(Boolean);
  }, []);
  const visible = scheduled
    .filter((t) => frame >= t.startFrame && frame < t.endFrame)
    .slice(0, 2);  // 最多同时 2 个
  return <>{visible.map((t, i) => <TermTooltip key={t.term} {...t} index={i} />)}</>;
};
```

### 设计要点

- 每个术语显示 5s，从屏幕顶部弹入
- 最多同时 2 个，避免遮挡主画面
- 避免知识的诅咒——对非技术观众友好

## 视频素材速度控制

```tsx
import { OffthreadVideo, staticFile } from "remotion";

<OffthreadVideo src={staticFile("demo.mp4")} playbackRate={2} />
```

| 素材类型 | 推荐速度 |
|---------|---------|
| 终端操作 | 2x-3x |
| GUI 录屏 | 1.5x-2x |
| 效果展示 | 1x-2x |
