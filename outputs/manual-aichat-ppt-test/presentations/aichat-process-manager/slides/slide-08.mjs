import { colors, slideBg, foot, card } from "./common.mjs";

export async function slide08(presentation, ctx) {
  const a = ctx.artifact;
  const slide = presentation.slides.add();
  slide.compose(a.layers({ width: 1280, height: 720 }, [
    ...slideBg(a, "核心功能模块"),
    ...card(a, 70, 190, 340, 132, "用户端", "登录注册、AI 角色选择、会话列表、聊天页、消息收藏、反馈提交、个人资料。", colors.sky),
    ...card(a, 470, 190, 340, 132, "角色维护端", "创建/编辑 AI 角色，查看角色使用统计与角色反馈。管理员继承该权限。", colors.amber),
    ...card(a, 870, 190, 340, 132, "管理后台", "用户管理、角色管理、消息审核、反馈管理、系统日志、全局统计。", colors.red),
    ...card(a, 170, 390, 410, 122, "过程数据展示", "消息详情弹窗展示正文块、推理过程、工具调用链、调用结果与模型元数据。", colors.purple),
    ...card(a, 700, 390, 410, 122, "业务闭环", "收藏用于沉淀高价值回复，反馈用于评价角色质量，后台统计用于观察整体使用情况。", colors.green),
    ...foot(a, 8),
  ]));
  return slide;
}
