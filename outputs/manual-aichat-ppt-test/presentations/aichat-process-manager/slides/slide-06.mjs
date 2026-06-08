import { colors, titleSlide, footer, card, text, box } from "./common.mjs";

export async function slide06(presentation, ctx) {
  const slide = presentation.slides.add();
  titleSlide(ctx, slide, "数据库设计：13 张核心表");
  card(ctx, slide, 70, 185, 260, 210, "身份与角色", "users\nai_characters", colors.blue);
  card(ctx, slide, 370, 185, 260, 210, "会话与消息", "conversations\nmessages\nmessage_contents", colors.green);
  card(ctx, slide, 670, 185, 260, 210, "AI 过程链", "message_reasoning\ntool_calls\ntool_results\nmessage_metadata", colors.purple);
  card(ctx, slide, 970, 185, 240, 210, "交互与治理", "message_favorites\nfeedbacks\nsystem_logs\naudit_records", colors.amber);
  box(ctx, slide, 115, 465, 1050, 96, colors.white, "#E2E8F0", 1);
  text(ctx, slide, "设计重点", 145, 490, 160, 28, 22, colors.ink, { bold: true });
  text(ctx, slide, "把“最终回复”拆成内容、推理、工具调用、工具结果、元数据；同时把用户行为和后台治理数据独立建表，便于查询、审计和扩展。", 285, 492, 790, 44, 18, colors.muted);
  footer(ctx, slide, 6);
  return slide;
}
