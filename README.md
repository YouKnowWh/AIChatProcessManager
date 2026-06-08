# AIChatProcessManager

管理"用户与 AI 角色的会话过程数据"的全栈课程设计项目，重点保存 AI 回复背后的完整过程链路（reasoning、tool_calls、tool_results、metadata）。

## 技术栈

| 层 | 技术 |
|------|------|
| 前端 | Vue 3 + Vite + TypeScript + Element Plus + Pinia |
| 后端 | Python + FastAPI + SQLAlchemy + Pydantic |
| 数据库 | MySQL |
| 鉴权 | JWT + bcrypt |
| 部署 | Docker Compose |

## 快速启动

```bash
# 1. 克隆仓库
git clone https://github.com/YouKnowWh/AIChatProcessManager.git
cd AIChatProcessManager

# 2. 配置环境变量（已提供默认值，直接可用）
cp .env.example .env

# 3. 前台启动（MySQL + 自动建表 + 填充测试数据）
docker compose up

# 4. 访问
# API 文档: http://localhost:8000/docs
# 健康检查: http://localhost:8000/api/health
```

> `.env` 已加入 `.gitignore`，仓库内提供 `.env.example` 作为模板。

## 项目结构

```
AIChatProcessManager/
├── backend/              # FastAPI 后端
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── main.py           # 应用入口，路由注册
│       ├── api/routes/       # 10 个路由模块
│       ├── core/             # config, security, deps
│       ├── db/               # SQLAlchemy engine
│       ├── models/           # 13 个 ORM 模型
│       ├── schemas/          # Pydantic schemas
│       ├── services/         # 业务逻辑
│       └── utils/            # APIResponse 等工具
├── database/             # MySQL 脚本
│   ├── schema.sql            # 13 张表完整 DDL
│   └── seed.sql              # 测试数据
├── docs/                 # 文档
│   └── database_design.md    # ER 图 + 表设计
├── docker-compose.yml    # MySQL + Backend 编排
├── .env.example          # 环境变量模板
└── .gitignore
```

## License

MIT
