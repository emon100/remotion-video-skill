# 3Blue1Brown 风格指南

借鉴 3B1B 的可视化设计原则，用于教程讲解类视频。

## 核心理念

让观众「自己发现」，而不是「被告知答案」。

| 原则 | 说明 | 示例 |
|------|------|------|
| **Why → What** | 先提问为什么，再展示是什么 | "如何识别手写数字？" → 展示神经网络 |
| **逐步构建** | 元素一个个出现，不要整体淡入 | 神经元依次点亮，而非同时出现 |
| **颜色有语义** | 颜色传达信息，不是装饰 | 蓝=正、红=负、黄=高亮 |
| **数值具象化** | 显示具体数字让抽象概念落地 | 像素值 0.7、激活值 0.92 |
| **2D 优先** | 清晰优先于炫酷，必要时才用 3D | 网络结构用 2D，空间数据用 3D |

## 配色方案

```tsx
const COLORS_3B1B = {
  background: "#000000",     // 纯黑背景
  positive: "#58C4DD",       // 蓝色 - 正权重
  negative: "#FF6B6B",       // 红色 - 负权重
  highlight: "#FFFF00",      // 黄色 - 当前焦点
  result: "#83C167",         // 绿色 - 结果
  text: "#FFFFFF",           // 白色 - 文字
  neutral: "#888888",        // 灰色 - 未激活
  accent: "#FF8C00",         // 橙色 - 强调
};
```

## 2D/3D 混合策略

| 内容类型 | 推荐维度 | 原因 |
|----------|----------|------|
| 网络结构图 | 2D | 层次清晰，易于标注 |
| 卷积操作 | 2D 俯视图 | 网格对齐，数值可见 |
| 特征图堆叠 | 2.5D（透视） | 展示深度/通道数 |
| 3D 物体识别 | 3D | 内容本身是 3D |

2D 模式用正交相机 + `<planeGeometry>` 实现。

## 逐步构建动画

用 `delay` + `spring` 控制元素依次出现：

```tsx
const StaggeredGroup: React.FC<{
  children: React.ReactNode[];
  delayPerItem?: number;
}> = ({ children, delayPerItem = 8 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <>
      {React.Children.map(children, (child, i) => {
        const delay = i * delayPerItem;
        const progress = spring({ frame: frame - delay, fps, config: { damping: 12, stiffness: 100 } });
        if (frame < delay) return null;
        return <group scale={Math.max(0, progress)}>{child}</group>;
      })}
    </>
  );
};
```

## 数值标签 & 高亮焦点

- **ValueLabel**：根据值正负选颜色（正=蓝、负=红、中性=灰），等宽字体显示 `value.toFixed(2)`
- **FocusBox**：脉冲高亮框引导注意力，`1 + Math.sin(frame * 0.15) * 0.08` 控制脉动

## 脚本撰写

**❌ 宣布式**："首先是输入层。图像是一个数字矩阵。"

**✅ 探索式**：
```
"你能轻松认出这是数字 7，但你能描述你是怎么做到的吗？
（停顿 1 秒）
这正是神经网络要解决的问题。
让我们先看看计算机「看到」的是什么——
（数字网格逐个显示）
不是图像，而是 784 个数字。"
```

**结构模板**：提出问题(10%) → 直觉猜测(15%) → 逐步验证(50%) → 形式化(15%) → 回顾总结(10%)

## 常见误区

| 误区 | 改进 |
|------|------|
| 3D 炫技 | 用最简单视角表达 |
| 颜色随意 | 建立颜色-含义映射 |
| 整体出现 | 逐个元素 + 高亮引导 |
| 只说 What | 先问 Why 再展示 What |
| 信息过载 | 一个场景一个概念 |
