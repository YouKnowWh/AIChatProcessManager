import { colors, titleSlide, footer, node, arrow, text, box } from "./common.mjs";

export async function slide03(presentation, ctx) {
  const slide = presentation.slides.add();
  titleSlide(ctx, slide, "三类角色与权限边界");
  node(ctx, slide, "普通用户", "发起会话、查看消息过程、收藏消息、提交反馈", 95, 215, 285, 170, colors.blue);
  arrow(ctx, slide, 400, 298, 95);
  node(ctx, slide, "角色维护者", "维护 AI 角色资料与状态，服务内容侧配置", 515, 215, 285, 170, colors.amber);
  arrow(ctx, slide, 820, 298, 95);
  node(ctx, slide, "管理员", "用户管理、消息管理、反馈、日志、统计，继承维护者能力", 935, 215, 285, 170, colors.purple);
  box(ctx, slide, 130, 455, 1020, 110, colors.white, "#E2E8F0", 1);
  text(ctx, slide, "为什么角色维护者和管理员不合并？", 160, 482, 520, 28, 22, colors.ink, { bold: true });
  text(ctx, slide, "角色维护是内容配置权限；管理员是平台治理权限。拆开可以避免“能改角色的人也能改用户、看日志、看统计”的越权问题。管理员继承维护能力，但维护者不能反向进入系统管理。", 160, 522, 900, 40, 17, colors.muted);
  footer(ctx, slide, 3);
  return slide;
}
