import { colors, box, text, chip, card } from "./common.mjs";

export async function slide11(presentation, ctx) {
  const slide = presentation.slides.add();
  box(ctx, slide, 0, 0, 1280, 720, "#0B1220");
  chip(ctx, slide, "Summary", 84, 76, "#93C5FD", 120);
  text(ctx, slide, "阶段总结与下一步", 84, 145, 760, 58, 48, colors.white, { bold: true });
  text(ctx, slide, "第一阶段已经完成核心模型、前后台页面、两级权限边界与可运行核验。", 88, 220, 850, 34, 22, "#DBEAFE");
  card(ctx, slide, 90, 330, 330, 145, "已经完成", "13 张表注册、前后端构建、Docker 编排、API 冒烟测试、关键业务 bug 修复。", colors.green);
  card(ctx, slide, 475, 330, 330, 145, "项目亮点", "不是普通聊天应用，而是把 AI 回复过程和用户自定义角色作为可管理数据资产沉淀下来。", colors.blue);
  card(ctx, slide, 860, 330, 330, 145, "后续扩展", "真实模型接入、流式响应、统计图表、更多审计策略和自动化测试。", colors.amber);
  text(ctx, slide, "Thank You", 86, 615, 340, 38, 30, "#BFDBFE", { bold: true });
  text(ctx, slide, "AIChatProcessManager", 860, 630, 330, 24, 16, "#93C5FD", { align: "right" });
  return slide;
}
