import { colors, titleSlide, footer, card, bullets } from "./common.mjs";

export async function slide02(presentation, ctx) {
  const slide = presentation.slides.add();
  titleSlide(ctx, slide, "项目要解决什么问题");
  card(ctx, slide, 70, 190, 340, 310, "传统 AI 对话系统", "通常只保留用户问题和最终回复，AI 在回复过程中的推理、工具调用、结果、元数据很难被复盘。", colors.red);
  card(ctx, slide, 470, 190, 340, 310, "本项目的核心目标", "把一次 AI 会话拆成可管理、可审计、可收藏、可反馈的数据链路，让过程数据真正进入业务系统。", colors.blue);
  card(ctx, slide, 870, 190, 340, 310, "管理端价值", "普通用户管理自己的 AI 角色与会话；管理员负责用户、角色状态、消息、反馈、日志和统计治理。", colors.green);
  bullets(ctx, slide, [
    "从“聊天页面”升级为“AI 会话过程管理平台”",
    "第一阶段重点：数据结构、权限边界、前后台完整运行",
    "为后续接入真实大模型、流式响应和统计分析留出接口"
  ], 120, 555, 980, 18);
  footer(ctx, slide, 2);
  return slide;
}
