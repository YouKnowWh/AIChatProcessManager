import { colors, titleSlide, footer, node, arrow, text, box } from "./common.mjs";

export async function slide03(presentation, ctx) {
  const slide = presentation.slides.add();
  titleSlide(ctx, slide, "两类用户角色与权限边界");
  node(ctx, slide, "普通用户", "聊天会话\n自定义 AI 角色\n收藏消息\n提交反馈\n查看个人统计", 170, 220, 320, 210, colors.blue);
  arrow(ctx, slide, 535, 322, 145);
  node(ctx, slide, "管理员", "用户管理\nAI 角色状态管理\n消息治理\n反馈处理\n日志与系统统计", 735, 220, 320, 210, colors.purple);
  box(ctx, slide, 130, 500, 1020, 96, colors.white, "#E2E8F0", 1);
  text(ctx, slide, "为什么合并“角色维护者”？", 160, 525, 360, 28, 22, colors.ink, { bold: true });
  text(ctx, slide, "它本质是用户侧自定义配置：普通用户维护自己的 AI 角色，管理员负责平台级审核和状态治理。这样角色体系更简单，答辩演示也更自然。", 500, 526, 570, 42, 17, colors.muted);
  footer(ctx, slide, 3);
  return slide;
}
