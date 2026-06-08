import { colors, slideBg, foot, node, arrow, txt, rect } from "./common.mjs";

export async function slide04(presentation, ctx) {
  const a = ctx.artifact;
  const slide = presentation.slides.add();
  slide.compose(a.layers({ width: 1280, height: 720 }, [
    ...slideBg(a, "核心业务流程：从会话创建到过程沉淀"),
    ...node(a, "登录鉴权", "JWT + bcrypt", 70, 235, 160, 120, colors.blue),
    ...arrow(a, 240, 294, 310, 294),
    ...node(a, "选择角色", "通用助手 / 代码专家 / 文档写手", 320, 235, 190, 120, colors.purple),
    ...arrow(a, 520, 294, 590, 294),
    ...node(a, "创建会话", "绑定 user_id 与 character_id", 600, 235, 190, 120, colors.sky),
    ...arrow(a, 800, 294, 870, 294),
    ...node(a, "发送消息", "用户消息 + AI 回复", 880, 235, 170, 120, colors.green),
    ...arrow(a, 1060, 294, 1120, 294),
    ...node(a, "过程入库", "正文 / 推理 / 工具 / 元数据", 1125, 235, 110, 120, colors.amber),
    rect(a, 96, 446, 1088, 96, colors.white, "#CBD5E1 1px", 8),
    txt(a, "沉淀后的数据可继续支撑：收藏复用、反馈评价、消息审核、系统统计、角色优化。", 146, 482, 980, 24, colors.ink, "font-weight: 800; alignment: center"),
    ...foot(a, 4),
  ]));
  return slide;
}
