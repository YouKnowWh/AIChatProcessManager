import { colors, titleSlide, footer, node, arrow, text } from "./common.mjs";

export async function slide04(presentation, ctx) {
  const slide = presentation.slides.add();
  titleSlide(ctx, slide, "核心业务流程");
  const y = 250;
  node(ctx, slide, "登录鉴权", "JWT 识别用户与角色", 60, y, 175, 130, colors.blue);
  arrow(ctx, slide, 252, y + 63, 55);
  node(ctx, slide, "选择 AI 角色", "通用助手 / 代码专家 / 文档写手", 325, y, 205, 130, colors.cyan);
  arrow(ctx, slide, 550, y + 63, 55);
  node(ctx, slide, "创建会话", "会话归属当前用户", 625, y, 180, 130, colors.green);
  arrow(ctx, slide, 825, y + 63, 55);
  node(ctx, slide, "发送消息", "保存用户消息和 AI 回复", 895, y, 185, 130, colors.amber);
  arrow(ctx, slide, 1098, y + 63, 45);
  node(ctx, slide, "过程入库", "reasoning / tools / metadata", 1150, y, 95, 130, colors.purple);
  text(ctx, slide, "流程闭环：消息可查看、可收藏、可反馈；后台可按用户、角色、消息、日志进行治理。", 125, 470, 1000, 34, 22, colors.ink, { bold: true, align: "center" });
  text(ctx, slide, "本轮已重点验证路由、权限、收藏状态、中文编码、消息详情与管理端接口。", 150, 520, 950, 26, 17, colors.muted, { align: "center" });
  footer(ctx, slide, 4);
  return slide;
}
