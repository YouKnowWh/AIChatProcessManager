import { colors, slideBg, foot, card, txt } from "./common.mjs";

export async function slide11(presentation, ctx) {
  const a = ctx.artifact;
  const slide = presentation.slides.add();
  slide.compose(a.layers({ width: 1280, height: 720 }, [
    ...slideBg(a, "总结与后续扩展"),
    ...card(a, 88, 185, 332, 168, "已完成", "全栈架构、13 张表数据模型、三类权限、会话消息过程链路、收藏反馈、管理后台、Docker 运行核验。", colors.green),
    ...card(a, 474, 185, 332, 168, "项目亮点", "围绕 AI 回复过程建模，把 reasoning、tool_calls、tool_results、metadata 从“不可见”变成“可管理”。", colors.blue),
    ...card(a, 860, 185, 332, 168, "可扩展方向", "真实大模型接入、流式输出、自动化测试、统计图表增强、审计策略和多租户权限。", colors.purple),
    txt(a, "一句话收束", 140, 450, 220, 24, colors.ink, "font-weight: 900"),
    txt(a, "AIChatProcessManager 的核心价值，是为 AI 应用建立一套可追踪、可审计、可运营的会话过程数据底座。", 140, 494, 1000, 30, colors.ink, "font-weight: 850; leading: 122"),
    ...foot(a, 11),
  ]));
  return slide;
}
