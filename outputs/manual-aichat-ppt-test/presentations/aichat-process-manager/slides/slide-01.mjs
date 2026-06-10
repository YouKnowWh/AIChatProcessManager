import { colors, box, text, chip, metric } from "./common.mjs";

export async function slide01(presentation, ctx) {
  const slide = presentation.slides.add();
  box(ctx, slide, 0, 0, 1280, 720, colors.navy);
  box(ctx, slide, 760, 0, 520, 720, "#1D4ED8");
  box(ctx, slide, 1040, 0, 240, 720, "#0F766E");
  chip(ctx, slide, "课程设计答辩", 84, 78, "#93C5FD", 150);
  text(ctx, slide, "AIChatProcessManager", 84, 158, 880, 70, 56, colors.white, { bold: true });
  text(ctx, slide, "AI 会话过程管理系统", 88, 238, 620, 42, 30, "#DBEAFE", { bold: true });
  text(ctx, slide, "面向 AI 回复过程链路的数据建模、权限管理与后台治理", 88, 308, 780, 34, 22, "#E0F2FE");
  box(ctx, slide, 84, 410, 930, 1, "#93C5FD88");
  metric(ctx, slide, "13", "核心数据表", 92, 462, "#FFFFFF");
  metric(ctx, slide, "2", "用户角色", 268, 462, "#FFFFFF");
  metric(ctx, slide, "10+", "API 模块", 444, 462, "#FFFFFF");
  metric(ctx, slide, "5", "过程数据维度", 620, 462, "#FFFFFF");
  text(ctx, slide, "Vue 3 / FastAPI / SQLAlchemy / MySQL / Docker Compose", 88, 650, 760, 24, 16, "#BFDBFE");
  text(ctx, slide, "Phase 1 可运行核验版", 970, 640, 230, 26, 16, "#D1FAE5", { align: "right", bold: true });
  return slide;
}
