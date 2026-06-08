import { colors, slideBg, foot, node, arrow, txt, rect } from "./common.mjs";

export async function slide03(presentation, ctx) {
  const a = ctx.artifact;
  const slide = presentation.slides.add();
  slide.compose(a.layers({ width: 1280, height: 720 }, [
    ...slideBg(a, "三类角色：权限继承但职责分离"),
    ...node(a, "普通用户", "会话、消息、收藏、反馈、个人统计", 95, 230, 245, 150, colors.sky),
    ...arrow(a, 360, 304, 455, 304),
    ...node(a, "角色维护者", "普通用户能力 + AI 角色维护、角色统计、角色反馈", 475, 230, 285, 150, colors.amber),
    ...arrow(a, 780, 304, 875, 304),
    ...node(a, "管理员", "角色维护者能力 + 用户管理、消息审核、系统日志、全局统计", 895, 230, 285, 150, colors.red),
    rect(a, 120, 458, 1040, 96, colors.white, "#E2E8F0 1px", 10),
    txt(a, "为什么不合并后两者？", 156, 482, 260, 22, colors.ink, "font-weight: 900"),
    txt(a, "角色维护者是内容运营权限，管理员是平台治理权限。合并会导致维护角色的人同时拥有禁用用户、查看全站消息、改系统数据的能力，权限过大。", 430, 480, 675, 18, colors.muted, "leading: 124"),
    ...foot(a, 3),
  ]));
  return slide;
}
