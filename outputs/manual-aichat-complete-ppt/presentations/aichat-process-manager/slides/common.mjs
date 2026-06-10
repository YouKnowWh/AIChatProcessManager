
export const W = 1280;
export const H = 720;

export const colors = {
  ink: "#0A0A0A",
  ink2: "#171717",
  graphite: "#333333",
  muted: "#5F6368",
  quiet: "#737373",
  paper: "#FAFAF8",
  paper2: "#FFFFFF",
  line: "#D4D4D2",
  cyan: "#002FA7",
  mint: "#002FA7",
  amber: "#737373",
  coral: "#A3A3A0",
  violet: "#002FA7",
  white: "#FFFFFF",
  deep: "#F0F0EE",
};

export const slides = [
  {
    "no": 1,
    "kind": "cover",
    "kicker": "COURSE DESIGN DEFENSE",
    "title": "AIChatProcessManager",
    "subtitle": "AI 会话过程管理系统",
    "body": "面向 AI 回复全过程链路的数据建模、功能设计、数据库设计与系统实现",
    "stats": [
      [
        "13",
        "核心数据表"
      ],
      [
        "10+",
        "API 模块"
      ],
      [
        "2",
        "用户角色"
      ],
      [
        "5",
        "过程维度"
      ]
    ],
    "sourceNo": 1
  },
  {
    "no": 2,
    "kind": "agenda",
    "kicker": "STORYLINE",
    "title": "内容结构按“背景与意义 → 技术框架 → 用户需求 → 功能设计 → 数据库设计 → 系统实现 → 总结反思”展开",
    "items": [
      "背景与意义",
      "技术框架",
      "用户需求与功能设计",
      "数据库设计",
      "系统实现与运行验证",
      "总结与反思"
    ],
    "sourceNo": 3
  },
  {
    "no": 3,
    "kind": "contrast",
    "kicker": "BACKGROUND",
    "title": "传统聊天系统只保存结果，不利于 AI 会话过程的管理、复盘与治理",
    "leftTitle": "普通聊天记录",
    "left": [
      "用户问题",
      "AI 最终回复",
      "少量时间戳"
    ],
    "rightTitle": "过程管理平台",
    "right": [
      "消息正文与多内容块",
      "reasoning 可见性控制",
      "工具调用参数与状态",
      "工具结果与错误信息",
      "模型 token / 时延 / finish reason"
    ],
    "note": "系统将回复链路拆分为独立数据对象，使消息生产、过程记录、质量回流与治理动作能够在同一套结构中持续沉淀。",
    "sourceNo": 4
  },
  {
    "no": 4,
    "kind": "thesis",
    "kicker": "CORE THESIS",
    "title": "系统价值不在“聊天”，而在把 AI 回复过程沉淀为可治理的数据资产",
    "body": "传统对话系统只保存问题与最终回复；本项目进一步记录 reasoning、tool calls、tool results、metadata、feedback 与 audit trail，让一次 AI 回复具备复盘、追踪、管理和扩展的基础。",
    "proof": [
      "过程可追踪",
      "权限可隔离",
      "反馈可回流",
      "治理可审计"
    ],
    "sourceNo": 2
  },
  {
    "no": 5,
    "kind": "architecture",
    "kicker": "TECH STACK",
    "title": "技术框架由前端、后端、数据库与部署环境四部分共同组成",
    "layers": [
      [
        "Vue 3 Frontend",
        "Element Plus\nPinia\nVite / TypeScript\n组件成熟 / 状态清晰"
      ],
      [
        "FastAPI Backend",
        "JWT / bcrypt\nService layer\nPydantic schemas\n接口组织简洁"
      ],
      [
        "MySQL 8.0",
        "13 tables\nutf8mb4\nseed data\n关系型约束稳定"
      ],
      [
        "Docker Compose",
        "Backend + DB\n环境变量\n可重复运行\n部署链路统一"
      ]
    ],
    "sourceNo": 7
  },
  {
    "no": 6,
    "kind": "api",
    "kicker": "TECH DETAIL",
    "title": "系统接口按身份、会话、交互与治理四类能力拆分，支撑模块化实现",
    "groups": [
      [
        "身份",
        "auth / users"
      ],
      [
        "角色",
        "characters"
      ],
      [
        "会话",
        "conversations / messages"
      ],
      [
        "交互",
        "favorites / feedbacks"
      ],
      [
        "治理",
        "admin / logs / stats"
      ]
    ],
    "note": "接口层通过统一前缀、分域路由和数据校验模型组织请求入口，使前后端联调路径、异常处理与权限控制保持一致。",
    "sourceNo": 8
  },
  {
    "no": 7,
    "kind": "roles",
    "kicker": "USER REQUIREMENT",
    "title": "用户需求首先体现在两类参与者及其不同的功能目标上",
    "roles": [
      [
        "普通用户",
        [
          "登录注册",
          "创建 AI 角色",
          "发起会话",
          "收藏消息",
          "提交反馈",
          "查看个人统计"
        ]
      ],
      [
        "管理员",
        [
          "用户状态管理",
          "角色状态治理",
          "消息治理",
          "反馈处理",
          "系统日志",
          "平台统计"
        ]
      ]
    ],
    "note": "系统将创作类能力保留在用户侧，将状态治理、审核与统计统一收拢到管理侧，以形成清晰的权限边界与责任划分。",
    "sourceNo": 5
  },
  {
    "no": 8,
    "kind": "flow",
    "kicker": "FUNCTION FLOW",
    "title": "核心功能围绕一次完整会话流程展开：从登录、发起会话到过程入库与治理闭环",
    "steps": [
      "JWT 登录",
      "选择角色",
      "创建会话",
      "发送消息",
      "AI 回复",
      "过程入库",
      "收藏/反馈",
      "后台治理"
    ],
    "note": "消息、收藏、反馈、日志都挂在同一套身份与消息链路上，便于复盘和权限校验。",
    "sourceNo": 6
  },
  {
    "no": 9,
    "kind": "permission",
    "kicker": "FUNCTION DESIGN",
    "title": "功能设计同时考虑用户权限隔离、管理员治理能力和历史数据一致性",
    "lanes": [
      [
        "用户侧",
        "只能访问自己的会话、消息、收藏和反馈"
      ],
      [
        "管理员侧",
        "可进入后台治理用户、角色、消息、反馈、日志和统计"
      ],
      [
        "数据侧",
        "角色删除改为禁用，历史会话仍保持引用完整"
      ]
    ],
    "sourceNo": 12
  },
  {
    "no": 10,
    "kind": "frontend",
    "kicker": "FUNCTION MODULE",
    "title": "前台功能模块围绕“角色 → 会话 → 消息详情 → 收藏/反馈”组织",
    "modules": [
      "登录注册",
      "角色列表",
      "会话列表",
      "聊天详情",
      "过程详情弹窗",
      "收藏中心",
      "个人资料"
    ],
    "note": "前台界面围绕角色浏览、会话管理、消息详情和反馈沉淀四条路径展开，界面状态与业务状态通过统一 store 管理保持同步。",
    "sourceNo": 13
  },
  {
    "no": 11,
    "kind": "feedback",
    "kicker": "FUNCTION DESIGN",
    "title": "收藏与反馈机制体现了功能设计中的质量回流与用户交互闭环",
    "steps": [
      "收藏消息",
      "提交反馈",
      "关联 message_id",
      "关联 character_id",
      "后台处理",
      "统计复盘"
    ],
    "note": "收藏与反馈数据构成用户侧质量回流入口，使系统能够从静态结果展示延伸到偏好分析、角色评估和内容优化。",
    "sourceNo": 15
  },
  {
    "no": 12,
    "kind": "database",
    "kicker": "DATABASE DESIGN",
    "title": "数据库设计围绕身份、会话、过程链路与治理数据四个域展开",
    "groups": [
      [
        "身份与角色",
        [
          "users",
          "ai_characters"
        ]
      ],
      [
        "会话与消息",
        [
          "conversations",
          "messages",
          "message_contents"
        ]
      ],
      [
        "AI 过程链",
        [
          "message_reasoning",
          "tool_calls",
          "tool_results",
          "message_metadata"
        ]
      ],
      [
        "交互与治理",
        [
          "message_favorites",
          "feedbacks",
          "system_logs",
          "audit_records"
        ]
      ]
    ],
    "sourceNo": 9
  },
  {
    "no": 13,
    "kind": "er",
    "kicker": "ER DIAGRAM",
    "title": "概念设计：ER 图展示核心实体及关系",
    "sourceNo": 26
  },
  {
    "no": 14,
    "kind": "processData",
    "kicker": "DATABASE CORE",
    "title": "数据库核心创新在于把 AI 回复拆成正文、推理、工具、结果和元数据五类过程证据",
    "nodes": [
      [
        "messages",
        "消息主干\nsender / role / status"
      ],
      [
        "contents",
        "正文块\ntext / markdown / code"
      ],
      [
        "reasoning",
        "推理摘要\nvisibility control"
      ],
      [
        "tool_calls",
        "名称 / 参数\n状态 / 时间"
      ],
      [
        "tool_results",
        "结果内容\n错误标记"
      ],
      [
        "metadata",
        "model / token\nlatency / finish"
      ]
    ],
    "sourceNo": 10
  },
  {
    "no": 15,
    "kind": "schema",
    "kicker": "LOGICAL DESIGN",
    "title": "逻辑设计上，主消息表保持稳定，变化快的过程细节通过子表扩展",
    "rows": [
      [
        "messages",
        "conversation_id, parent_message_id, sender_type, role, sequence_number",
        "承载会话顺序与父子关系，并作为其他过程表的主关联中心"
      ],
      [
        "message_contents",
        "content_type, content, sort_order",
        "支持多段正文排序展示，便于后续扩展富文本、多模态或附件内容"
      ],
      [
        "message_reasoning",
        "reasoning_content, visibility",
        "控制过程信息可见范围，兼顾展示需要与敏感信息隔离"
      ],
      [
        "tool_calls",
        "tool_name, arguments, status, called_at",
        "记录工具调用参数、调用时点与执行状态，支撑过程复盘"
      ],
      [
        "message_metadata",
        "model_name, tokens, duration_ms, finish_reason",
        "支撑成本统计、性能分析、模型对比与质量评估"
      ]
    ],
    "sourceNo": 11
  },
  {
    "no": 16,
    "kind": "admin",
    "kicker": "SYSTEM IMPLEMENTATION",
    "title": "系统实现不只包括前台页面，后台治理端也是完整平台的重要组成部分",
    "modules": [
      "用户管理",
      "角色管理",
      "消息管理",
      "反馈管理",
      "系统日志",
      "统计看板"
    ],
    "note": "后台界面以状态治理、反馈处理、日志追踪和统计分析为核心，覆盖平台运行后的主要管理动作与证据留存。",
    "sourceNo": 14
  },
  {
    "no": 17,
    "kind": "audit",
    "kicker": "SYSTEM IMPLEMENTATION",
    "title": "日志与审核能力让系统实现层面具备可追踪、可治理、可扩展的基础",
    "points": [
      [
        "system_logs",
        "记录 action、target_type、target_id、detail、ip_address"
      ],
      [
        "audit_records",
        "记录 admin_id、target、action 与 comment"
      ],
      [
        "status fields",
        "users / characters / conversations / messages 均具备状态位"
      ]
    ],
    "sourceNo": 16
  },
  {
    "no": 18,
    "kind": "adapter",
    "kicker": "SYSTEM IMPLEMENTATION",
    "title": "模型适配层与失败回退机制保证系统演示稳定，也为后续接入真实模型留出接口",
    "stages": [
      "请求上下文",
      "角色提示词",
      "模型调用",
      "失败回退",
      "过程映射",
      "消息入库"
    ],
    "note": "适配层负责把上下文、模型调用结果、工具调用信息和性能元数据映射到既有表结构中，保持系统接口与数据层的一致性。",
    "sourceNo": 17
  },
  {
    "no": 19,
    "kind": "deployment",
    "kicker": "DEPLOYMENT",
    "title": "运行环境通过 Docker Compose 完成编排，覆盖配置、数据、服务与文档四个交付面",
    "blocks": [
      [
        "配置",
        ".env.example\n默认变量"
      ],
      [
        "数据库",
        "schema.sql\nseed.sql\nutf8mb4"
      ],
      [
        "后端",
        "FastAPI\nSQLAlchemy\n健康检查"
      ],
      [
        "文档",
        "README\nAPI docs\n数据库设计"
      ]
    ],
    "sourceNo": 18
  },
  {
    "no": 20,
    "kind": "verification",
    "kicker": "SYSTEM VERIFICATION",
    "title": "系统实现已经从“能构建”推进到“主要业务链路可运行”",
    "checks": [
      [
        "后端导入",
        "路由注册与 ORM 模型可加载"
      ],
      [
        "前端构建",
        "Vue 3 + TypeScript + Vite production build"
      ],
      [
        "API 冒烟",
        "健康检查、鉴权、消息、收藏、反馈路径"
      ],
      [
        "数据核验",
        "中文 seed 数据与 utf8mb4 编码"
      ]
    ],
    "sourceNo": 19
  },
  {
    "no": 21,
    "kind": "fixes",
    "kicker": "IMPLEMENTATION DETAIL",
    "title": "在系统实现过程中，关键问题集中在路由、编码、权限和数据一致性修正上",
    "fixes": [
      [
        "路由前缀",
        "messages / users / favorites / feedbacks 统一为 /api"
      ],
      [
        "中文编码",
        "MySQL、SQLAlchemy、seed 统一 utf8mb4"
      ],
      [
        "收藏状态",
        "消息列表返回 is_favorited，切换页面后保持状态"
      ],
      [
        "权限隔离",
        "用户不能读取、收藏或反馈别人的消息"
      ],
      [
        "数据保留",
        "角色删除改为禁用，保护历史会话引用"
      ],
      [
        "配置健壮性",
        "DEBUG=release 可解析，模型失败可回退"
      ],
      [
        "索引与约束",
        "主外键关联、状态字段与排序字段共同保证查询效率与结构稳定性"
      ]
    ],
    "sourceNo": 20
  },
  {
    "no": 22,
    "kind": "demo",
    "kicker": "DEMO ROUTE",
    "title": "系统展示路径覆盖用户使用链路与后台治理链路",
    "steps": [
      "登录 user1 / admin",
      "查看角色与会话",
      "进入聊天详情",
      "展开过程数据",
      "收藏并返回验证",
      "提交反馈",
      "进入管理后台",
      "展示日志与统计"
    ],
    "sourceNo": 23
  },
  {
    "no": 23,
    "kind": "metrics",
    "kicker": "WORK SUMMARY",
    "title": "从表结构、接口模块到前后台页面，项目规模已具备完整课程设计的工作量",
    "stats": [
      [
        "13",
        "ORM / DDL 核心表"
      ],
      [
        "10+",
        "后端路由模块"
      ],
      [
        "18+",
        "前端视图"
      ],
      [
        "6",
        "后台治理页"
      ],
      [
        "5",
        "AI 过程数据维度"
      ]
    ],
    "sourceNo": 21
  },
  {
    "no": 24,
    "kind": "risk",
    "kicker": "REFLECTION",
    "title": "本项目的收获与反思主要体现在权限设计、数据治理和可扩展性意识上",
    "risks": [
      [
        "推理敏感性",
        "visibility 字段控制 reasoning 暴露范围"
      ],
      [
        "工具结果可信度",
        "tool_results 保留 is_error 与原始 JSON"
      ],
      [
        "历史数据破坏",
        "角色禁用替代物理删除"
      ],
      [
        "模型接入不稳定",
        "DeepSeek 调用失败回退模拟 AI"
      ],
      [
        "中文数据质量",
        "数据库连接和 seed 均使用 utf8mb4"
      ]
    ],
    "sourceNo": 22
  },
  {
    "no": 25,
    "kind": "roadmap",
    "kicker": "REFLECTION",
    "title": "系统后续扩展方向集中在模型接入、分析能力、治理策略与自动化测试",
    "phases": [
      [
        "真实模型",
        "DeepSeek / OpenAI\nstreaming / tool calls"
      ],
      [
        "分析看板",
        "token 成本\n延迟趋势\n角色质量"
      ],
      [
        "治理策略",
        "审核流\n敏感内容\n可见性策略"
      ],
      [
        "自动化测试",
        "API 回归\n权限用例\n前端 E2E"
      ]
    ],
    "sourceNo": 24
  },
  {
    "no": 26,
    "kind": "summary",
    "kicker": "SUMMARY",
    "title": "本项目完成了从需求分析到数据库设计、系统实现与运行验证的完整闭环",
    "bullets": [
      "完整链路：问题、回复、推理、工具、结果、元数据都可保存。",
      "工程闭环：前端、后端、数据库、Docker 与文档形成可运行系统。",
      "治理闭环：用户行为、反馈、日志、审核与统计都进入后台。",
      "扩展闭环：真实模型、流式响应、质量分析可沿当前模型继续实现。"
    ],
    "sourceNo": 25
  },
  {
    "no": 27,
    "kind": "thanks",
    "kicker": "THANK YOU",
    "title": "谢谢",
    "subtitle": "AIChatProcessManager",
    "body": "感谢观看",
    "stats": [
      [
        "Vue 3",
        "Frontend"
      ],
      [
        "FastAPI",
        "Backend"
      ],
      [
        "MySQL",
        "Database"
      ],
      [
        "Docker",
        "Runtime"
      ]
    ],
    "sourceNo": 27
  }
];
export const assets = {
  processChain: "/Users/alex/Projects/AIChatProcessManager/outputs/manual-aichat-complete-ppt/presentations/aichat-process-manager/assets/10-process-chain.png",
  adminConsole: "/Users/alex/Projects/AIChatProcessManager/outputs/manual-aichat-complete-ppt/presentations/aichat-process-manager/assets/14-admin-console.png",
  verificationBoard: "/Users/alex/Projects/AIChatProcessManager/outputs/manual-aichat-complete-ppt/presentations/aichat-process-manager/assets/19-verification-board.png",
  erDiagram: "/Users/alex/Projects/AIChatProcessManager/outputs/manual-aichat-complete-ppt/presentations/aichat-process-manager/assets/ig_02afd613b312915a016a27d0ca305c8191a3290a7590be1f0d.png",
};

export function box(ctx, slide, left, top, width, height, fill = colors.white, line = "#00000000", lineWidth = 0) {
  return ctx.addShape(slide, { left, top, width, height, fill, line: ctx.line(line, lineWidth) });
}

export function text(ctx, slide, value, left, top, width, height, fontSize = 22, color = colors.ink, opts = {}) {
  return ctx.addText(slide, {
    text: String(value ?? ""),
    left, top, width, height, fontSize, color,
    bold: Boolean(opts.bold),
    align: opts.align ?? "left",
    valign: opts.valign ?? "top",
    typeface: opts.face ?? "PingFang SC",
    fill: "#00000000",
    line: ctx.line("#00000000", 0),
    insets: opts.insets ?? { left: 0, right: 0, top: 0, bottom: 0 },
  });
}

export function line(ctx, slide, left, top, width, height = 2, color = colors.line) {
  return box(ctx, slide, left, top, width, height, color);
}

export function bg(ctx, slide, dark = false) {
  box(ctx, slide, 0, 0, W, H, dark ? colors.deep : colors.paper);
  box(ctx, slide, 0, 0, W, 720, dark ? "#F5F5F2" : colors.paper);
  line(ctx, slide, 84, 0, 1, 720, colors.line);
  line(ctx, slide, 930, 0, 1, 720, "#ECECEA");
  line(ctx, slide, 1188, 0, 1, 720, "#F0F0EE");
}

export function footer(ctx, slide, no, dark = false) {
  const c = colors.quiet;
  text(ctx, slide, "课程设计答辩 | AI 会话过程管理系统", 104, 682, 520, 20, 11, c);
  text(ctx, slide, String(no).padStart(2, "0"), 1180, 682, 38, 20, 11, c, { align: "right" });
}

export function header(ctx, slide, spec, dark = false) {
  const k = colors.cyan;
  box(ctx, slide, 104, 54, 8, 8, k);
  text(ctx, slide, spec.kicker, 122, 46, 280, 22, 11, k, { bold: true });
  text(ctx, slide, spec.title, 104, 92, 920, 74, 31, colors.ink, { bold: true });
  line(ctx, slide, 104, 174, 1040, 1, colors.line);
}

export function pill(ctx, slide, value, left, top, width, color = colors.cyan, dark = false) {
  box(ctx, slide, left, top, width, 30, dark ? color + "33" : color + "1F", color, 1.2);
  text(ctx, slide, value, left + 12, top + 8, width - 24, 14, 11, color, { bold: true, align: "center" });
}

export function panel(ctx, slide, left, top, width, height, title, body, color = colors.cyan, dark = false) {
  box(ctx, slide, left, top + 6, 4, height - 12, color);
  text(ctx, slide, title, left + 20, top + 10, width - 32, 28, 18, colors.ink, { bold: true });
  text(ctx, slide, body, left + 20, top + 46, width - 32, height - 52, 14, colors.muted);
}

export function stat(ctx, slide, value, label, left, top, color = colors.cyan, dark = false) {
  text(ctx, slide, value, left, top, 145, 46, 35, color, { bold: true, align: "center" });
  text(ctx, slide, label, left, top + 48, 145, 24, 12, colors.muted, { align: "center" });
}

function arrow(ctx, slide, left, top, width, color = colors.cyan) {
  line(ctx, slide, left, top, width, 2.5, color);
  ctx.addShape(slide, { geometry: "triangle", left: left + width - 5, top: top - 7, width: 15, height: 15, fill: color, line: ctx.line(color, 0) });
}

function bulletList(ctx, slide, items, left, top, width, color = colors.ink, accent = colors.cyan, gap = 38, size = 17) {
  items.forEach((item, i) => {
    box(ctx, slide, left, top + i * gap + 8, 7, 7, accent);
    text(ctx, slide, item, left + 20, top + i * gap, width - 20, gap + 8, size, color);
  });
}

async function imageCard(ctx, slide, imagePath, left, top, width, height) {
  line(ctx, slide, left, top, width, 1, colors.line);
  line(ctx, slide, left, top + height, width, 1, colors.line);
  await ctx.addImage(slide, {
    path: imagePath,
    left: left + 6,
    top: top + 10,
    width: width - 12,
    height: height - 20,
    fit: "contain",
  });
}

function renderCover(ctx, slide, spec) {
  bg(ctx, slide, true);
  pill(ctx, slide, spec.kicker, 86, 72, 190, colors.cyan, true);
  text(ctx, slide, spec.title, 86, 154, 820, 78, 56, colors.ink, { bold: true });
  text(ctx, slide, spec.subtitle, 90, 244, 600, 44, 31, colors.cyan, { bold: true });
  text(ctx, slide, spec.body, 90, 318, 820, 58, 22, colors.graphite);
  text(ctx, slide, "课程名称：数据库课程设计    学生姓名：XXX    学号：XXXXXXXX    专业班级：XXXX", 90, 386, 860, 26, 16, colors.muted);
  text(ctx, slide, "内容覆盖背景与意义、技术框架、用户需求、功能设计、数据库设计、系统实现、总结反思与致谢，展示系统从建模到落地的完整过程。", 90, 418, 820, 44, 17, colors.muted);
  line(ctx, slide, 90, 456, 900, 1, colors.line);
  spec.stats.forEach((s, i) => stat(ctx, slide, s[0], s[1], 98 + i * 180, 500, colors.cyan, true));
  text(ctx, slide, "Vue 3 / FastAPI / SQLAlchemy / MySQL / Docker Compose", 90, 648, 740, 22, 15, colors.muted);
}

function renderThesis(ctx, slide, spec) {
  bg(ctx, slide, true);
  header(ctx, slide, spec, true);
  text(ctx, slide, spec.body, 110, 232, 830, 112, 23, colors.graphite);
  spec.proof.forEach((p, i) => {
    const x = 116 + i * 252;
    box(ctx, slide, x, 430, 206, 92, colors.paper2, colors.line, 1);
    text(ctx, slide, "0" + (i + 1), x + 18, 448, 42, 26, 16, colors.cyan, { bold: true });
    text(ctx, slide, p, x + 62, 444, 110, 34, 22, colors.ink, { bold: true });
  });
  footer(ctx, slide, spec.no, true);
}

function renderAgenda(ctx, slide, spec) {
  bg(ctx, slide, false);
  header(ctx, slide, spec);
  spec.items.forEach((item, i) => {
    const y = 218 + i * 66;
    text(ctx, slide, String(i + 1).padStart(2, "0"), 122, y, 46, 28, 22, [colors.cyan, colors.mint, colors.amber, colors.coral, colors.violet, colors.graphite][i], { bold: true });
    line(ctx, slide, 180, y + 13, 80, 1.5, colors.line);
    text(ctx, slide, item, 286, y - 2, 690, 30, 25, colors.ink, { bold: true });
  });
  footer(ctx, slide, spec.no);
}

function renderContrast(ctx, slide, spec) {
  bg(ctx, slide, false);
  header(ctx, slide, spec);
  panel(ctx, slide, 116, 228, 430, 270, spec.leftTitle, spec.left.join("\n"), colors.coral);
  panel(ctx, slide, 660, 202, 470, 326, spec.rightTitle, spec.right.join("\n"), colors.cyan);
  text(ctx, slide, spec.note, 120, 570, 960, 40, 18, colors.graphite);
  footer(ctx, slide, spec.no);
}

function renderRoles(ctx, slide, spec) {
  bg(ctx, slide, false);
  header(ctx, slide, spec);
  spec.roles.forEach((role, i) => {
    const x = i === 0 ? 132 : 676;
    panel(ctx, slide, x, 218, 448, 294, role[0], role[1].join("\n"), i === 0 ? colors.mint : colors.violet);
  });
  text(ctx, slide, spec.note, 150, 568, 950, 36, 18, colors.graphite);
  footer(ctx, slide, spec.no);
}

function renderFlow(ctx, slide, spec) {
  bg(ctx, slide, false);
  header(ctx, slide, spec);
  spec.steps.forEach((s, i) => {
    const x = 112 + (i % 4) * 270;
    const y = i < 4 ? 246 : 420;
    box(ctx, slide, x, y + 8, 4, 42, colors.cyan);
    text(ctx, slide, String(i + 1).padStart(2, "0"), x + 18, y + 10, 34, 24, 18, colors.cyan, { bold: true });
    text(ctx, slide, s, x + 62, y + 10, 140, 26, 18, colors.ink, { bold: true });
    text(ctx, slide, i < 4 ? "前台动作" : "治理闭环", x + 62, y + 38, 120, 18, 11, colors.muted);
    if (i !== 3 && i !== 7) arrow(ctx, slide, x + 202, y + 36, 48, colors.quiet);
  });
  text(ctx, slide, spec.note, 130, 572, 970, 34, 18, colors.graphite);
  footer(ctx, slide, spec.no);
}

function renderArchitecture(ctx, slide, spec) {
  bg(ctx, slide, true);
  header(ctx, slide, spec, true);
  spec.layers.forEach((l, i) => {
    const x = 100 + i * 287;
    panel(ctx, slide, x, 258, 230, 210, l[0], l[1], [colors.cyan, colors.mint, colors.amber, colors.coral][i], true);
    if (i < spec.layers.length - 1) arrow(ctx, slide, x + 242, 365, 42, colors.cyan);
  });
  footer(ctx, slide, spec.no, true);
}

function renderApi(ctx, slide, spec) {
  bg(ctx, slide, false);
  header(ctx, slide, spec);
  spec.groups.forEach((g, i) => {
    const x = 112 + i * 214;
    panel(ctx, slide, x, 244, 178, 184, g[0], g[1], [colors.cyan, colors.mint, colors.amber, colors.coral, colors.violet][i]);
  });
  text(ctx, slide, spec.note, 124, 536, 960, 36, 18, colors.graphite);
  footer(ctx, slide, spec.no);
}

function renderDatabase(ctx, slide, spec) {
  bg(ctx, slide, false);
  header(ctx, slide, spec);
  spec.groups.forEach((g, i) => {
    const x = 116 + (i % 2) * 525;
    const y = 216 + Math.floor(i / 2) * 180;
    panel(ctx, slide, x, y, 430, 132, g[0], g[1].join("  /  "), [colors.cyan, colors.mint, colors.amber, colors.violet][i]);
  });
  footer(ctx, slide, spec.no);
}

async function renderProcessData(ctx, slide, spec) {
  bg(ctx, slide, true);
  header(ctx, slide, spec, true);
  await imageCard(ctx, slide, assets.processChain, 104, 220, 760, 318);
  text(ctx, slide, "过程链路图展示了消息从生成到沉淀的完整拆分方式。系统没有把回复压缩为单条文本，而是拆成正文、推理、工具、结果和元数据等多个可管理对象。", 892, 236, 248, 120, 18, colors.graphite);
  bulletList(ctx, slide, ["消息主干负责顺序和归属", "过程信息独立建表，便于扩展", "过程表之间通过 message_id / tool_call_id 形成关联"], 892, 374, 236, colors.ink, colors.cyan, 46, 15);
  footer(ctx, slide, spec.no, true);
}

function renderSchema(ctx, slide, spec) {
  bg(ctx, slide, false);
  header(ctx, slide, spec);
  const x = 104, y = 212;
  box(ctx, slide, x, y, 1038, 52, colors.cyan, colors.cyan, 0);
  text(ctx, slide, "表", x + 18, y + 17, 150, 18, 13, colors.white, { bold: true });
  text(ctx, slide, "关键字段", x + 220, y + 17, 430, 18, 13, colors.white, { bold: true });
  text(ctx, slide, "设计作用", x + 700, y + 17, 300, 18, 13, colors.white, { bold: true });
  spec.rows.forEach((r, i) => {
    const yy = y + 52 + i * 62;
    box(ctx, slide, x, yy, 1038, 62, i % 2 ? "#F0F0EE" : colors.paper2, colors.line, 0.8);
    text(ctx, slide, r[0], x + 18, yy + 19, 170, 18, 14, colors.cyan, { bold: true });
    text(ctx, slide, r[1], x + 220, yy + 15, 420, 30, 13, colors.graphite);
    text(ctx, slide, r[2], x + 700, yy + 15, 300, 30, 13, colors.graphite);
  });
  footer(ctx, slide, spec.no);
}

function renderPermission(ctx, slide, spec) {
  bg(ctx, slide, false);
  header(ctx, slide, spec);
  spec.lanes.forEach((lane, i) => {
    const y = 240 + i * 108;
    text(ctx, slide, lane[0], 126, y + 22, 130, 26, 20, [colors.cyan, colors.violet, colors.amber][i], { bold: true });
    line(ctx, slide, 274, y + 34, 80, 2, colors.line);
    panel(ctx, slide, 386, y, 650, 74, "", lane[1], [colors.cyan, colors.violet, colors.amber][i]);
  });
  footer(ctx, slide, spec.no);
}

async function renderModuleGrid(ctx, slide, spec, dark = false) {
  bg(ctx, slide, dark);
  header(ctx, slide, spec, dark);
  if (spec.no === 14) {
    await imageCard(ctx, slide, assets.adminConsole, 104, 220, 740, 340);
    text(ctx, slide, "后台界面将用户、角色、消息、反馈、日志和统计等治理对象统一组织在同一管理面中，便于完成状态处理、问题定位和运行观察。", 872, 236, 260, 108, 18, colors.graphite);
    bulletList(ctx, slide, ["导航区域按治理域划分模块", "中部图表表达系统运行状态", "底部列表承接待处理数据与最新记录"], 872, 366, 244, colors.ink, colors.cyan, 46, 15);
    footer(ctx, slide, spec.no, dark);
    return;
  }
  spec.modules.forEach((m, i) => {
    const x = 120 + (i % 4) * 250;
    const y = 246 + Math.floor(i / 4) * 114;
    box(ctx, slide, x, y + 8, 4, 42, colors.cyan);
    text(ctx, slide, m, x + 18, y + 10, 160, 24, 18, colors.ink, { bold: true });
    line(ctx, slide, x + 18, y + 52, 150, 1, colors.line);
  });
  text(ctx, slide, spec.note ?? "", 126, 560, 970, 36, 18, colors.graphite);
  footer(ctx, slide, spec.no, dark);
}

function renderFeedback(ctx, slide, spec) {
  bg(ctx, slide, false);
  header(ctx, slide, spec);
  spec.steps.forEach((s, i) => {
    const x = 126 + i * 168;
    text(ctx, slide, String(i + 1), x, 320, 32, 30, 26, colors.cyan, { bold: true });
    text(ctx, slide, s, x + 34, 320, 98, 24, 15, colors.ink, { bold: true });
    line(ctx, slide, x + 34, 354, 82, 1, colors.line);
    if (i < spec.steps.length - 1) arrow(ctx, slide, x + 132, 372, 30, colors.quiet);
  });
  text(ctx, slide, spec.note, 130, 540, 950, 38, 18, colors.graphite);
  footer(ctx, slide, spec.no);
}

function renderAudit(ctx, slide, spec) {
  bg(ctx, slide, true);
  header(ctx, slide, spec, true);
  spec.points.forEach((p, i) => panel(ctx, slide, 130, 232 + i * 120, 900, 82, p[0], p[1], [colors.cyan, colors.amber, colors.coral][i], true));
  footer(ctx, slide, spec.no, true);
}

function renderAdapter(ctx, slide, spec) {
  bg(ctx, slide, false);
  header(ctx, slide, spec);
  spec.stages.forEach((s, i) => {
    const x = 108 + i * 176;
    panel(ctx, slide, x, 284, 132, 106, s, "", [colors.cyan, colors.mint, colors.amber, colors.coral, colors.violet, colors.graphite][i]);
    if (i < spec.stages.length - 1) arrow(ctx, slide, x + 142, 337, 26, colors.quiet);
  });
  text(ctx, slide, spec.note, 126, 536, 960, 42, 18, colors.graphite);
  footer(ctx, slide, spec.no);
}

function renderDeployment(ctx, slide, spec) {
  bg(ctx, slide, false);
  header(ctx, slide, spec);
  spec.blocks.forEach((b, i) => panel(ctx, slide, 126 + i * 254, 256, 202, 180, b[0], b[1], [colors.cyan, colors.mint, colors.amber, colors.violet][i]));
  footer(ctx, slide, spec.no);
}

async function renderVerification(ctx, slide, spec) {
  bg(ctx, slide, true);
  header(ctx, slide, spec, true);
  await imageCard(ctx, slide, assets.verificationBoard, 104, 220, 740, 340);
  text(ctx, slide, "验证页将数据库、接口、页面、日志和运行记录放在同一组证据中展示，用于说明系统已经形成可构建、可访问、可验证的工程闭环。", 872, 236, 260, 108, 18, colors.graphite);
  spec.checks.forEach((c, i) => {
    const y = 356 + i * 48;
    text(ctx, slide, c[0], 872, y, 96, 18, 15, colors.cyan, { bold: true });
    text(ctx, slide, c[1], 972, y, 160, 28, 14, colors.graphite);
  });
  footer(ctx, slide, spec.no, true);
}

function renderFixes(ctx, slide, spec) {
  bg(ctx, slide, false);
  header(ctx, slide, spec);
  spec.fixes.forEach((f, i) => {
    const x = 112 + (i % 2) * 520;
    const y = 220 + Math.floor(i / 2) * 108;
    panel(ctx, slide, x, y, 430, 62, f[0], f[1], colors.cyan);
  });
  footer(ctx, slide, spec.no);
}

function renderMetrics(ctx, slide, spec) {
  bg(ctx, slide, true);
  header(ctx, slide, spec, true);
  spec.stats.forEach((s, i) => {
    const x = 108 + i * 210;
    box(ctx, slide, x, 302, 166, 134, colors.paper2, colors.line, 1);
    stat(ctx, slide, s[0], s[1], x + 10, 330, colors.cyan, true);
  });
  footer(ctx, slide, spec.no, true);
}

function renderRisk(ctx, slide, spec) {
  bg(ctx, slide, false);
  header(ctx, slide, spec);
  spec.risks.forEach((r, i) => {
    const y = 220 + i * 70;
    text(ctx, slide, r[0], 126, y + 12, 190, 24, 17, [colors.cyan, colors.mint, colors.amber, colors.coral, colors.violet][i], { bold: true });
    text(ctx, slide, r[1], 360, y + 12, 660, 24, 17, colors.graphite);
    line(ctx, slide, 126, y + 52, 900, 1, colors.line);
  });
  footer(ctx, slide, spec.no);
}

function renderDemo(ctx, slide, spec) {
  bg(ctx, slide, false);
  header(ctx, slide, spec);
  spec.steps.forEach((s, i) => {
    const x = 106 + (i % 4) * 268;
    const y = 236 + Math.floor(i / 4) * 166;
    text(ctx, slide, String(i + 1).padStart(2, "0"), x, y + 18, 40, 24, 18, colors.cyan, { bold: true });
    text(ctx, slide, s, x + 48, y + 18, 132, 42, 17, colors.ink, { bold: true });
    line(ctx, slide, x + 48, y + 62, 118, 1, colors.line);
  });
  footer(ctx, slide, spec.no);
}

function renderRoadmap(ctx, slide, spec) {
  bg(ctx, slide, true);
  header(ctx, slide, spec, true);
  spec.phases.forEach((p, i) => {
    const x = 118 + i * 260;
    panel(ctx, slide, x, 260, 204, 142, p[0], p[1], colors.cyan, true);
    text(ctx, slide, "0" + (i + 1), x + 144, 214, 52, 30, 23, colors.cyan, { bold: true, align: "right" });
  });
  footer(ctx, slide, spec.no, true);
}

function renderSummary(ctx, slide, spec) {
  bg(ctx, slide, false);
  header(ctx, slide, spec);
  bulletList(ctx, slide, spec.bullets, 130, 244, 900, colors.ink, colors.cyan, 70, 21);
  footer(ctx, slide, spec.no);
}

async function renderEr(ctx, slide, spec) {
  bg(ctx, slide, false);
  header(ctx, slide, spec);
  await ctx.addImage(slide, {
    path: assets.erDiagram,
    left: 118,
    top: 208,
    width: 1036,
    height: 352,
    fit: "contain",
  });
  footer(ctx, slide, spec.no);
}

function renderThanks(ctx, slide, spec) {
  bg(ctx, slide, true);
  pill(ctx, slide, spec.kicker, 86, 74, 118, colors.cyan, true);
  text(ctx, slide, spec.title, 86, 166, 420, 94, 74, colors.ink, { bold: true });
  text(ctx, slide, spec.subtitle, 90, 278, 620, 44, 32, colors.cyan, { bold: true });
  text(ctx, slide, spec.body, 90, 362, 760, 50, 22, colors.graphite);
  spec.stats.forEach((s, i) => stat(ctx, slide, s[0], s[1], 112 + i * 184, 514, colors.cyan, true));
}

function narrativeCopy(spec) {
  const key = spec.sourceNo ?? spec.no;
  const extra = {
    1: "本页概括系统主题、课程信息与项目范围，突出本项目围绕 AI 会话过程管理展开，覆盖数据建模、功能设计、数据库设计与系统实现几个核心层面。",
    2: "整套内容按照背景与意义、技术框架、用户需求、功能设计、数据库设计、系统实现与总结反思几个层次组织，形成从问题提出到系统落地的连续结构。",
    3: "传统聊天系统更偏向结果展示，而本系统进一步关注回复形成过程中的结构化证据、行为记录、质量回流与平台治理需求，以提升数据可管理性。",
    4: "系统核心不在单次问答展示，而在于把上下文、推理、工具调用、结果与反馈信号沉淀为可追踪、可治理、可分析的数据对象，形成过程化数据资产。",
    5: "技术选型同时考虑开发效率、维护成本、生态成熟度与扩展空间，使前端交互、后端接口、关系型存储与部署编排之间保持稳定分工与清晰边界。",
    6: "接口层按身份、会话、交互和治理分域组织，统一前缀、参数校验与异常处理方式，有助于后续模块扩展、权限控制与前后端联调的一致性。",
    7: "需求分析从参与角色入手，分别描述用户侧使用诉求与管理侧治理诉求，进一步明确角色边界、功能范围以及系统在使用层与管理层的职责分工。",
    8: "业务流程覆盖登录、会话创建、消息发送、过程入库、收藏反馈和后台治理，完整展示数据从交互产生到记录沉淀再到治理处理的流转路径。",
    9: "功能设计不仅包含页面操作，也覆盖权限隔离、状态约束与历史引用完整性等规则层设计，使前台使用逻辑与后台治理逻辑建立一致的数据边界。",
    10: "前台功能围绕角色浏览、会话操作、消息查看和反馈沉淀展开，形成用户侧主要使用路径，并通过统一状态管理保持身份信息和页面行为同步。",
    11: "收藏与反馈数据补充了消息使用后的行为证据，为质量分析、角色评估、内容优化和用户偏好观察提供可持续积累的基础数据来源。",
    12: "数据库总览从数据域角度组织表结构，体现身份数据、会话数据、过程数据与治理数据之间的整体关系，并为后续 ER 图与逻辑设计提供基础。",
    13: "ER 图用于说明核心实体之间的主外键关系，集中展示用户、角色、会话、消息及过程子表之间的连接方式，是数据库概念设计层的中心视图。",
    14: "过程建模将一次 AI 回复拆成多个实体对象，使正文、推理、工具、结果和元数据可以分别存储和复用，从而支持过程追踪、结果复盘和能力扩展。",
    15: "逻辑设计通过主表与子表配合保持核心结构稳定，同时为多内容块、过程信息、性能数据和工具结果等变化更快的对象预留扩展空间。",
    16: "后台模块覆盖用户、角色、消息、反馈、日志和统计几个治理域，体现平台化系统的完整管理面，也补足系统在运行后的管理能力与审计能力。",
    17: "日志与审核记录为状态变更、问题定位和平台留痕提供基础支撑，同时通过动作、目标、详情和时间等字段形成治理过程中的操作证据。",
    18: "适配层将模型返回内容映射到现有表结构中，使系统在模拟模式与真实模型模式下都能保持数据一致性，并为流式响应与工具调用预留接口位置。",
    19: "部署结构覆盖配置文件、数据库脚本、服务实例与文档资源，体现环境初始化、数据准备、服务启动与重复运行能力，保证系统可复现与可交付。",
    20: "运行验证从构建、接口、页面与数据几个维度展示系统状态，把数据库、接口调用、页面结构和日志记录放在同一组证据中形成实现闭环。",
    21: "关键修正集中在路由规范、编码统一、权限隔离、收藏状态保持、历史数据保护以及索引约束等工程细节上，体现系统联调和修正过程的完整性。",
    22: "展示路径按用户链路与管理链路展开，覆盖前台使用动作、后台治理动作和过程数据查看入口，使系统功能结构与页面组织之间形成清晰映射。",
    23: "表数量、接口模块、前后台页面与过程维度共同构成项目工作量，也反映出系统在数据层、接口层、页面层与治理层上的实现范围与复杂度。",
    24: "反思部分集中在权限意识、数据治理、过程建模和扩展能力几个方面，体现系统设计不只关注当前功能，也关注长期维护与后续演进空间。",
    25: "系统已经形成从需求、功能、数据、实现到验证的完整闭环，各层设计之间具备稳定映射关系，也为后续功能扩展和性能优化保留了清晰空间。",
    26: "ER 图集中展示用户、角色、会话、消息及过程子表之间的主外键关系，用于说明数据库概念设计层的核心实体结构与关联方式。",
    27: "结尾页用于收束整套展示内容，回到系统名称、技术栈和整体完成度，形成简洁稳定的结束画面并保持全稿视觉风格的一致性。"
  };
  return extra[key] || spec.note || spec.body || "";
}

function narrativeBand(ctx, slide, spec) {
  const copy = narrativeCopy(spec);
  if (!copy) return;
  line(ctx, slide, 104, 598, 1040, 1, colors.line);
  box(ctx, slide, 104, 610, 4, 24, colors.cyan);
  text(ctx, slide, copy, 126, 601, 986, 44, 14, colors.graphite, { valign: "middle" });
}

export async function renderSlide(presentation, ctx, slideNo) {
  const spec = slides[slideNo - 1];
  const slide = presentation.slides.add();
  switch (spec.kind) {
    case "cover": renderCover(ctx, slide, spec); break;
    case "thesis": renderThesis(ctx, slide, spec); break;
    case "agenda": renderAgenda(ctx, slide, spec); break;
    case "contrast": renderContrast(ctx, slide, spec); break;
    case "roles": renderRoles(ctx, slide, spec); break;
    case "flow": renderFlow(ctx, slide, spec); break;
    case "architecture": renderArchitecture(ctx, slide, spec); break;
    case "api": renderApi(ctx, slide, spec); break;
    case "database": renderDatabase(ctx, slide, spec); break;
    case "processData": await renderProcessData(ctx, slide, spec); break;
    case "schema": renderSchema(ctx, slide, spec); break;
    case "permission": renderPermission(ctx, slide, spec); break;
    case "frontend": await renderModuleGrid(ctx, slide, spec, false); break;
    case "admin": await renderModuleGrid(ctx, slide, spec, true); break;
    case "feedback": renderFeedback(ctx, slide, spec); break;
    case "audit": renderAudit(ctx, slide, spec); break;
    case "adapter": renderAdapter(ctx, slide, spec); break;
    case "deployment": renderDeployment(ctx, slide, spec); break;
    case "verification": await renderVerification(ctx, slide, spec); break;
    case "fixes": renderFixes(ctx, slide, spec); break;
    case "metrics": renderMetrics(ctx, slide, spec); break;
    case "risk": renderRisk(ctx, slide, spec); break;
    case "demo": renderDemo(ctx, slide, spec); break;
    case "roadmap": renderRoadmap(ctx, slide, spec); break;
    case "summary": renderSummary(ctx, slide, spec); break;
    case "er": await renderEr(ctx, slide, spec); break;
    case "thanks": renderThanks(ctx, slide, spec); break;
  }
  narrativeBand(ctx, slide, spec);
  return slide;
}
