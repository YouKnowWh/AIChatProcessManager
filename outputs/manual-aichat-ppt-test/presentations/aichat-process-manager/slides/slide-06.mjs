import { colors, slideBg, foot, txt, rect } from "./common.mjs";

function cluster(a, title, items, x, y, color) {
  return [
    rect(a, x, y, 250, 170, colors.white, `${color} 1.5px`, 10),
    rect(a, x, y, 250, 38, color, "none", 8),
    txt(a, title, x + 18, y + 10, 214, 16, colors.white, "font-weight: 800; alignment: center"),
    ...items.map((item, i) => txt(a, `• ${item}`, x + 24, y + 56 + i * 24, 200, 14, colors.ink)),
  ];
}

export async function slide06(presentation, ctx) {
  const a = ctx.artifact;
  const slide = presentation.slides.add();
  slide.compose(a.layers({ width: 1280, height: 720 }, [
    ...slideBg(a, "数据库设计：13 张表覆盖会话过程全链路"),
    ...cluster(a, "身份与角色", ["users", "ai_characters", "audit_records"], 78, 185, colors.blue),
    ...cluster(a, "会话与消息", ["conversations", "messages", "message_contents"], 380, 185, colors.green),
    ...cluster(a, "AI 过程数据", ["message_reasoning", "tool_calls", "tool_results", "message_metadata"], 682, 185, colors.purple),
    ...cluster(a, "互动与运营", ["message_favorites", "feedbacks", "system_logs"], 984, 185, colors.amber),
    rect(a, 132, 440, 1016, 92, colors.white, "#E2E8F0 1px", 10),
    txt(a, "设计重点", 168, 466, 120, 22, colors.ink, "font-weight: 900"),
    txt(a, "messages 只保存消息主干；正文、推理、工具调用、结果、模型元数据拆表存储，既减少主表膨胀，也便于按需展示与审计。", 306, 462, 780, 18, colors.muted, "leading: 126"),
    ...foot(a, 6),
  ]));
  return slide;
}
