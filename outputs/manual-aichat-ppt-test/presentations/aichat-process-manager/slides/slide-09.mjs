import { colors, titleSlide, footer, bullets, box, text } from "./common.mjs";

export async function slide09(presentation, ctx) {
  const slide = presentation.slides.add();
  titleSlide(ctx, slide, "业务逻辑核验与修正");
  box(ctx, slide, 75, 180, 1130, 385, colors.white, "#E2E8F0", 1);
  bullets(ctx, slide, [
    "路由前缀统一：messages / users / favorites / feedbacks 修正为 /api 路径，解决 Not Found。",
    "中文编码修正：MySQL、SQLAlchemy、seed 数据统一 utf8mb4，清理页面乱码。",
    "收藏状态持久化：消息列表返回 is_favorited，切换页面后仍显示“已收藏”。",
    "权限隔离：用户不能读取、收藏或反馈别人的消息；维护者不能进入管理员接口。",
    "角色删除改为禁用：避免物理删除影响历史会话数据。",
    "登录提示时长缩短：成功消息 1 秒自动消失，避免挡住页面操作。"
  ], 120, 215, 980, 18, colors.ink, 50);
  text(ctx, slide, "核验结论：第一阶段已经从“能构建”推进到“主要业务链路可运行”。", 120, 605, 960, 30, 21, colors.green, { bold: true });
  footer(ctx, slide, 9);
  return slide;
}
