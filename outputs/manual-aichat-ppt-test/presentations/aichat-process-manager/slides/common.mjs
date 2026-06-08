export const W = 1280;
export const H = 720;

export const colors = {
  ink: "#111827",
  muted: "#64748B",
  line: "#D8E0EA",
  bg: "#F6F8FB",
  navy: "#111827",
  blue: "#2563EB",
  cyan: "#06B6D4",
  green: "#16A34A",
  amber: "#F59E0B",
  red: "#DC2626",
  purple: "#7C3AED",
  white: "#FFFFFF",
  paleBlue: "#EFF6FF",
  paleGreen: "#ECFDF5",
  paleAmber: "#FFFBEB",
};

export function box(ctx, slide, left, top, width, height, fill = colors.white, line = "#00000000", lineWidth = 0) {
  return ctx.addShape(slide, {
    left,
    top,
    width,
    height,
    fill,
    line: ctx.line(line, lineWidth),
  });
}

export function text(ctx, slide, value, left, top, width, height, fontSize = 22, color = colors.ink, opts = {}) {
  return ctx.addText(slide, {
    text: value,
    left,
    top,
    width,
    height,
    fontSize,
    color,
    bold: Boolean(opts.bold),
    align: opts.align ?? "left",
    valign: opts.valign ?? "top",
    typeface: opts.face ?? "PingFang SC",
    fill: "#00000000",
    line: ctx.line("#00000000", 0),
    insets: opts.insets ?? { left: 0, right: 0, top: 0, bottom: 0 },
  });
}

export function titleSlide(ctx, slide, title, kicker = "AIChatProcessManager") {
  box(ctx, slide, 0, 0, W, H, colors.bg);
  box(ctx, slide, 0, 0, W, 78, colors.white);
  box(ctx, slide, 0, 77, W, 1, "#E5EAF2");
  text(ctx, slide, kicker, 56, 25, 380, 24, 16, colors.blue, { bold: true });
  text(ctx, slide, title, 56, 104, 900, 52, 34, colors.ink, { bold: true });
}

export function footer(ctx, slide, index, note = "课程设计答辩 | AI 会话过程管理系统") {
  text(ctx, slide, note, 56, 684, 640, 20, 12, "#94A3B8");
  text(ctx, slide, String(index).padStart(2, "0"), 1186, 684, 40, 20, 12, "#94A3B8", { align: "right" });
}

export function chip(ctx, slide, value, left, top, color = colors.blue, width = 138) {
  box(ctx, slide, left, top, width, 34, `${color}18`, color, 1);
  text(ctx, slide, value, left + 12, top + 8, width - 24, 18, 13, color, { bold: true, align: "center" });
}

export function card(ctx, slide, left, top, width, height, heading, body, color = colors.blue) {
  box(ctx, slide, left, top, width, height, colors.white, "#E2E8F0", 1);
  box(ctx, slide, left, top, 6, height, color);
  text(ctx, slide, heading, left + 24, top + 22, width - 48, 28, 21, colors.ink, { bold: true });
  text(ctx, slide, body, left + 24, top + 62, width - 48, height - 78, 15, colors.muted);
}

export function metric(ctx, slide, value, label, left, top, color = colors.blue) {
  text(ctx, slide, value, left, top, 150, 50, 40, color, { bold: true, align: "center" });
  text(ctx, slide, label, left, top + 50, 150, 28, 14, colors.muted, { align: "center" });
}

export function node(ctx, slide, heading, body, left, top, width, height, color = colors.blue) {
  box(ctx, slide, left, top, width, height, colors.white, color, 1.4);
  box(ctx, slide, left, top, width, 7, color);
  text(ctx, slide, heading, left + 14, top + 22, width - 28, 28, 19, colors.ink, { bold: true, align: "center" });
  text(ctx, slide, body, left + 18, top + 58, width - 36, height - 66, 13, colors.muted, { align: "center" });
}

export function arrow(ctx, slide, left, top, width, color = "#94A3B8") {
  box(ctx, slide, left, top, width, 3, color);
  ctx.addShape(slide, {
    geometry: "triangle",
    left: left + width - 4,
    top: top - 7,
    width: 16,
    height: 16,
    fill: color,
    line: ctx.line(color, 0),
  });
}

export function bullets(ctx, slide, items, left, top, width, fontSize = 19, color = colors.ink, gap = 38) {
  items.forEach((item, i) => {
    box(ctx, slide, left, top + i * gap + 7, 8, 8, colors.blue);
    text(ctx, slide, item, left + 24, top + i * gap, width - 24, gap + 8, fontSize, color);
  });
}
