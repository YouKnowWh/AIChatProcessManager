import { colors, slideBg, foot, txt, rect } from "./common.mjs";

function step(a, n, title, body, x, y, color) {
  return [
    rect(a, x, y, 230, 152, colors.white, "#E2E8F0 1px", 10),
    rect(a, x + 18, y + 18, 34, 34, color, "none", 17),
    txt(a, String(n), x + 18, y + 26, 34, 15, colors.white, "font-weight: 900; alignment: center"),
    txt(a, title, x + 66, y + 23, 140, 19, colors.ink, "font-weight: 850"),
    txt(a, body, x + 24, y + 70, 178, 14, colors.muted, "leading: 120"),
  ];
}

export async function slide10(presentation, ctx) {
  const a = ctx.artifact;
  const slide = presentation.slides.add();
  slide.compose(a.layers({ width: 1280, height: 720 }, [
    ...slideBg(a, "答辩演示路线"),
    ...step(a, 1, "普通用户登录", "展示首页、会话列表、角色标签与基础菜单。", 68, 195, colors.sky),
    ...step(a, 2, "创建会话", "从 AI 角色页进入聊天，发送消息并查看回复。", 326, 195, colors.blue),
    ...step(a, 3, "查看过程", "打开消息详情，展示 reasoning、工具调用和 metadata。", 584, 195, colors.purple),
    ...step(a, 4, "互动闭环", "收藏消息、切换页面后回到会话，验证已收藏状态恢复。", 842, 195, colors.green),
    ...step(a, 5, "管理员后台", "切换 admin，展示用户管理、消息管理、反馈与统计。", 455, 410, colors.red),
    txt(a, "演示重点：不要只展示“能聊天”，要突出“过程数据被结构化管理”。", 216, 600, 848, 24, colors.ink, "font-weight: 850; alignment: center"),
    ...foot(a, 10),
  ]));
  return slide;
}
