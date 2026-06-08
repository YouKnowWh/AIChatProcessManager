import { colors, slideBg, foot, txt, rect } from "./common.mjs";

function row(a, y, item, rule, result, color) {
  return [
    rect(a, 92, y, 1096, 54, colors.white, "#E2E8F0 1px", 6),
    txt(a, item, 118, y + 17, 260, 16, colors.ink, "font-weight: 800"),
    txt(a, rule, 406, y + 17, 420, 15, colors.muted),
    txt(a, result, 878, y + 17, 250, 15, color, "font-weight: 800"),
  ];
}

export async function slide09(presentation, ctx) {
  const a = ctx.artifact;
  const slide = presentation.slides.add();
  slide.compose(a.layers({ width: 1280, height: 720 }, [
    ...slideBg(a, "业务逻辑核验：演示前已修正的关键风险"),
    txt(a, "核验项", 118, 178, 180, 14, colors.muted, "font-weight: 800"),
    txt(a, "业务规则", 406, 178, 180, 14, colors.muted, "font-weight: 800"),
    txt(a, "当前结果", 878, 178, 180, 14, colors.muted, "font-weight: 800"),
    ...row(a, 205, "路由前缀", "前端统一请求 /api/...；FastAPI 路由全部挂载到 /api", "Not Found 已清理", colors.green),
    ...row(a, 270, "中文字符", "MySQL 初始化和 PyMySQL 连接统一 utf8mb4", "乱码已修复", colors.green),
    ...row(a, 335, "收藏状态", "消息列表返回 is_favorited；切换页面后恢复状态", "可持久显示", colors.green),
    ...row(a, 400, "权限隔离", "只能访问、收藏、反馈自己会话里的消息", "越权返回 403", colors.green),
    ...row(a, 465, "角色删除", "业务删除改为禁用，保留历史会话关联", "避免外键 500", colors.green),
    ...foot(a, 9),
  ]));
  return slide;
}
