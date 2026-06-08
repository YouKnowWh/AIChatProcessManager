import { colors, titleSlide, footer, node, arrow, text } from "./common.mjs";

export async function slide07(presentation, ctx) {
  const slide = presentation.slides.add();
  titleSlide(ctx, slide, "消息过程数据链路");
  node(ctx, slide, "messages", "一条用户或 AI 消息", 80, 235, 175, 130, colors.blue);
  arrow(ctx, slide, 270, 298, 55);
  node(ctx, slide, "contents", "文本 / 图片 / 文件等内容块", 340, 235, 190, 130, colors.cyan);
  arrow(ctx, slide, 550, 298, 55);
  node(ctx, slide, "reasoning", "模型思考过程摘要", 620, 235, 180, 130, colors.purple);
  arrow(ctx, slide, 818, 298, 55);
  node(ctx, slide, "tool calls", "调用名称、参数、状态", 888, 235, 175, 130, colors.amber);
  arrow(ctx, slide, 1080, 298, 45);
  node(ctx, slide, "results", "工具返回结果与耗时", 1140, 235, 100, 130, colors.green);
  text(ctx, slide, "附加元数据：token、模型、延迟、质量标签等写入 message_metadata。", 150, 455, 980, 28, 22, colors.ink, { bold: true, align: "center" });
  text(ctx, slide, "这样后续接入真实模型时，不需要重做表结构，只需要把生成过程映射到既有链路。", 160, 505, 960, 26, 17, colors.muted, { align: "center" });
  footer(ctx, slide, 7);
  return slide;
}
