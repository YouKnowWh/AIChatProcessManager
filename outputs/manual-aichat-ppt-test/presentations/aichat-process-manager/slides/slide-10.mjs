import { colors, titleSlide, footer, node, arrow, text, box } from "./common.mjs";

export async function slide10(presentation, ctx) {
  const slide = presentation.slides.add();
  titleSlide(ctx, slide, "演示路线建议");
  node(ctx, slide, "1. 登录", "user1 / manager / admin", 80, 220, 185, 120, colors.blue);
  arrow(ctx, slide, 285, 278, 55);
  node(ctx, slide, "2. 会话列表", "查看中文数据与角色名称", 360, 220, 205, 120, colors.green);
  arrow(ctx, slide, 585, 278, 55);
  node(ctx, slide, "3. 聊天详情", "查看消息和过程数据", 660, 220, 200, 120, colors.cyan);
  arrow(ctx, slide, 880, 278, 55);
  node(ctx, slide, "4. 收藏恢复", "收藏后切换页面再返回", 955, 220, 205, 120, colors.amber);
  box(ctx, slide, 125, 430, 1030, 110, colors.white, "#E2E8F0", 1);
  text(ctx, slide, "管理员补充演示", 155, 458, 240, 28, 22, colors.ink, { bold: true });
  text(ctx, slide, "进入管理后台，依次展示用户管理、角色管理、消息管理、反馈管理、系统日志和统计页面，说明管理员与角色维护者的权限差异。", 360, 460, 710, 44, 18, colors.muted);
  footer(ctx, slide, 10);
  return slide;
}
