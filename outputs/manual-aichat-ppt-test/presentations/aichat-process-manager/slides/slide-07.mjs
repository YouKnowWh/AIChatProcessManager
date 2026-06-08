import { colors, slideBg, foot, node, arrow, txt } from "./common.mjs";

export async function slide07(presentation, ctx) {
  const a = ctx.artifact;
  const slide = presentation.slides.add();
  slide.compose(a.layers({ width: 1280, height: 720 }, [
    ...slideBg(a, "消息过程链路：把 AI 回复从黑盒拆开保存"),
    ...node(a, "messages", "消息主表：角色、序号、状态", 78, 248, 160, 120, colors.blue),
    ...arrow(a, 250, 306, 312, 306),
    ...node(a, "contents", "多段正文：text / code / markdown", 322, 248, 170, 120, colors.sky),
    ...arrow(a, 505, 306, 567, 306),
    ...node(a, "reasoning", "推理过程：可见性控制", 577, 248, 170, 120, colors.purple),
    ...arrow(a, 760, 306, 822, 306),
    ...node(a, "tool calls", "工具名、参数、状态、call_id", 832, 248, 170, 120, colors.amber),
    ...arrow(a, 1015, 306, 1077, 306),
    ...node(a, "metadata", "模型、tokens、耗时、finish_reason", 1087, 248, 150, 120, colors.green),
    txt(a, "展示层支持：普通消息流 + 详情弹窗。详情页可查看 reasoning、tool_calls、tool_results、metadata，适合答辩演示“过程管理”的核心差异。", 122, 472, 1036, 24, colors.ink, "font-weight: 750; alignment: center; leading: 125"),
    ...foot(a, 7),
  ]));
  return slide;
}
