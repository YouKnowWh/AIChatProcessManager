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

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env 填入实际值

# 3. 启动服务
docker compose up -d

# 4. 初始化数据库
docker compose exec backend python init_db.py

# 5. 访问
# 前端: http://localhost:5173
# API 文档: http://localhost:8000/docs
```

## 项目结构

```
AIChatProcessManager/
├── backend/          # FastAPI 后端
│   └── app/
│       ├── api/routes/    # 路由
│       ├── core/          # 配置、安全、依赖
│       ├── db/            # 数据库连接
│       ├── models/        # SQLAlchemy 模型
│       ├── schemas/       # Pydantic schemas
│       ├── services/      # 业务逻辑
│       └── utils/         # 工具函数
├── frontend/         # Vue 3 前端
│   └── src/
│       ├── api/           # API 请求
│       ├── components/    # 组件
│       ├── layouts/       # 布局
│       ├── router/        # 路由
│       ├── stores/        # Pinia 状态
│       └── views/         # 页面
├── database/         # SQL 脚本
│   ├── schema.sql    # 建表
│   └── seed.sql      # 测试数据
└── docs/             # 文档
```

## License

MIT
