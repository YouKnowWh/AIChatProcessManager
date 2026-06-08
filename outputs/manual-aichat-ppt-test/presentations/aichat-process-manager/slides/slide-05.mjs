import { colors, slideBg, foot, node, arrow, txt, rect } from "./common.mjs";

export async function slide05(presentation, ctx) {
  const a = ctx.artifact;
  const slide = presentation.slides.add();
  slide.compose(a.layers({ width: 1280, height: 720 }, [
    ...slideBg(a, "系统架构：Vue 前端 + FastAPI 服务 + MySQL 数据层"),
    ...node(a, "Vue 3 前端", "Vite / TypeScript / Element Plus / Pinia", 90, 205, 250, 132, colors.sky),
    ...arrow(a, 360, 270, 455, 270),
    ...node(a, "FastAPI 后端", "REST API / Pydantic / JWT / Service 层", 475, 205, 300, 132, colors.blue),
    ...arrow(a, 795, 270, 890, 270),
    ...node(a, "MySQL 8.0", "13 张表 / utf8mb4 / 外键约束", 910, 205, 250, 132, colors.green),
    rect(a, 100, 430, 310, 82, "#EFF6FF", "#BFDBFE 1px", 8),
    txt(a, "前端职责", 125, 452, 120, 18, colors.blue, "font-weight: 800"),
    txt(a, "页面路由、状态管理、权限入口、交互反馈", 125, 480, 240, 14, colors.muted),
    rect(a, 485, 430, 310, 82, "#F5F3FF", "#DDD6FE 1px", 8),
    txt(a, "后端职责", 510, 452, 120, 18, colors.purple, "font-weight: 800"),
    txt(a, "鉴权、权限校验、业务编排、统一 API 响应", 510, 480, 245, 14, colors.muted),
    rect(a, 870, 430, 310, 82, "#ECFDF5", "#BBF7D0 1px", 8),
    txt(a, "数据职责", 895, 452, 120, 18, colors.green, "font-weight: 800"),
    txt(a, "过程数据持久化、关联查询、统计分析", 895, 480, 245, 14, colors.muted),
    ...foot(a, 5),
  ]));
  return slide;
}
