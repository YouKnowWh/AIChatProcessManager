import { colors, slideBg, foot, card } from "./common.mjs";

export async function slide02(presentation, ctx) {
  const a = ctx.artifact;
  const slide = presentation.slides.add();
  slide.compose(a.layers({ width: 1280, height: 720 }, [
    ...slideBg(a, "项目要解决的问题"),
    ...card(a, 64, 190, 330, 250, "普通聊天系统的问题", "只保存最终回答，缺少 AI 回复背后的推理、工具调用、模型元数据，后续无法审计、复盘或做质量评估。", colors.red),
    ...card(a, 475, 190, 330, 250, "课程设计的目标", "围绕“用户 - AI 角色 - 会话 - 消息过程”建模，完整保存正文、reasoning、tool_calls、tool_results 与 metadata。", colors.blue),
    ...card(a, 886, 190, 330, 250, "管理侧的价值", "支持角色维护、消息审核、反馈分析、用户管理和系统统计，让 AI 会话过程从黑盒变成可管理资产。", colors.green),
    ...card(a, 168, 500, 944, 86, "核心论点", "本项目不是简单聊天 Demo，而是一个面向 AI 会话过程数据治理的全栈管理系统。", colors.purple),
    ...foot(a, 2),
  ]));
  return slide;
}
