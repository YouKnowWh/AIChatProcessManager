import { colors, titleSlide, footer, card } from "./common.mjs";

export async function slide08(presentation, ctx) {
  const slide = presentation.slides.add();
  titleSlide(ctx, slide, "功能模块划分");
  card(ctx, slide, 80, 185, 330, 145, "前台会话", "登录注册、角色选择、会话列表、聊天详情、消息过程展示、收藏。", colors.blue);
  card(ctx, slide, 475, 185, 330, 145, "角色维护", "AI 角色列表、状态管理、资料维护；由角色维护者和管理员进入。", colors.amber);
  card(ctx, slide, 870, 185, 330, 145, "后台治理", "用户、消息、反馈、系统日志、统计；仅管理员进入。", colors.purple);
  card(ctx, slide, 80, 395, 330, 145, "交互反馈", "收藏消息、提交反馈、查看反馈状态，形成用户侧质量信号。", colors.green);
  card(ctx, slide, 475, 395, 330, 145, "审计日志", "系统操作留痕，支持后续课程展示中的安全与治理说明。", colors.cyan);
  card(ctx, slide, 870, 395, 330, 145, "可扩展接口", "真实 LLM、流式响应、统计图表、权限细化都可在当前结构上继续扩展。", colors.red);
  footer(ctx, slide, 8);
  return slide;
}
