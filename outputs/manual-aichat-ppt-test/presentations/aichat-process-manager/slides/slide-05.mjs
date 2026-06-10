import { colors, titleSlide, footer, node, arrow, card } from "./common.mjs";

export async function slide05(presentation, ctx) {
  const slide = presentation.slides.add();
  titleSlide(ctx, slide, "系统架构");
  node(ctx, slide, "Vue 3 前端", "Element Plus 组件\nPinia 状态管理\nVite production build", 95, 220, 275, 175, colors.blue);
  arrow(ctx, slide, 400, 305, 110);
  node(ctx, slide, "FastAPI 后端", "JWT 鉴权\nService 分层\nREST API", 545, 220, 275, 175, colors.green);
  arrow(ctx, slide, 850, 305, 110);
  node(ctx, slide, "MySQL 8.0", "13 张核心表\nutf8mb4 中文支持\n种子数据", 995, 220, 210, 175, colors.amber);
  card(ctx, slide, 115, 475, 465, 100, "部署与运行", "Docker Compose 编排 MySQL / Backend / Frontend；当前说明已改为前台运行，避免后台进程和 watch/reload 模式。", colors.purple);
  card(ctx, slide, 690, 475, 465, 100, "工程验证", "后端导入、ORM 表注册、前端 TypeScript、Vite 构建均已通过；真实模型适配层支持失败回退。", colors.cyan);
  footer(ctx, slide, 5);
  return slide;
}
