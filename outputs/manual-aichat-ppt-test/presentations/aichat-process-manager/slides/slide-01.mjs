import { W, H, colors, txt, rect, metric, chip } from "./common.mjs";

export async function slide01(presentation, ctx) {
  const { layers } = ctx.artifact;
  const a = ctx.artifact;
  const slide = presentation.slides.add();
  slide.compose(layers({ width: W, height: H }, [
    rect(a, 0, 0, W, H, colors.navy),
    rect(a, 0, 0, W, 720, "#0F172A"),
    rect(a, 704, 0, 576, 720, "#1E3A8A"),
    rect(a, 984, 0, 296, 720, "#0F766E"),
    ...chip(a, "课程设计答辩", 82, 74, "#93C5FD"),
    txt(a, "AIChatProcessManager", 80, 150, 900, 58, colors.white, "font-weight: 900"),
    txt(a, "AI 会话过程管理系统", 84, 226, 680, 30, "#C7D2FE", "font-weight: 650"),
    txt(a, "面向 AI 回复过程链路的数据建模、权限管理与后台治理", 84, 290, 800, 22, "#E0F2FE"),
    rect(a, 80, 410, 960, 1, "#93C5FD80"),
    ...metric(a, "13", "核心数据表", 90, 455, "#FFFFFF"),
    ...metric(a, "3", "权限角色", 300, 455, "#FFFFFF"),
    ...metric(a, "10+", "API 模块", 510, 455, "#FFFFFF"),
    ...metric(a, "5", "过程数据维度", 720, 455, "#FFFFFF"),
    txt(a, "Vue 3 / FastAPI / SQLAlchemy / MySQL / Docker Compose", 84, 650, 760, 16, "#BFDBFE"),
  ]));
  return slide;
}
