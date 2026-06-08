export async function slide01(presentation, ctx) {
  const { layers, text, shape } = ctx.artifact;
  const slide = presentation.slides.add();
  slide.compose(layers({ width: 1280, height: 720 }, [
    shape({ fill: "#0F172A", width: 1280, height: 720, position: { x: 0, y: 0 } }),
    text("AIChatProcessManager", {
      position: { x: 80, y: 100 },
      width: 800,
      style: "font-size: 54px; font-weight: bold; color: #FFFFFF; family: PingFang SC",
    }),
    text("AI 会话过程管理系统", {
      position: { x: 84, y: 180 },
      width: 600,
      style: "font-size: 28px; color: #93C5FD; family: PingFang SC",
    }),
  ]));
  return slide;
}
