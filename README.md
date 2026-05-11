# George 的极客空间

一个现代化的个人极客网站，展示数据科学与全栈开发的技术能力。

## 技术栈

### 前端
- Vue 3 (Composition API + `<script setup>`)
- Vite + Vue Router
- Tailwind CSS
- Pinia 状态管理
- Axios HTTP 客户端
- marked + highlight.js (Markdown 渲染)

### 后端
- Python 3 + FastAPI
- SQLAlchemy ORM
- SQLite 数据库
- SSE 实时推送

## 项目结构

```
geek-site/
├── frontend/                 # Vue 3 前端
│   ├── src/
│   │   ├── components/      # 组件
│   │   │   ├── common/      # 通用组件
│   │   │   ├── home/        # 首页组件
│   │   │   ├── docs/         # 文档组件
│   │   │   └── admin/       # 管理组件
│   │   ├── views/          # 页面视图
│   │   ├── composables/     # 组合式函数
│   │   ├── stores/          # Pinia 状态
│   │   ├── services/        # API 服务
│   │   └── router/          # 路由配置
│   └── package.json
├── backend/                  # FastAPI 后端
│   ├── app/
│   │   ├── models/         # 数据库模型
│   │   ├── schemas/        # Pydantic 模型
│   │   └── routers/        # API 路由
│   └── requirements.txt
└── README.md
```

## 快速开始

### 前端

```bash
cd frontend
npm install
npm run dev
```

访问 http://localhost:3000

### 后端

```bash
cd backend
pip install -r requirements.txt
python init_db.py  # 初始化数据库
python run.py      # 启动服务器
```

API 运行在 http://localhost:8000

## 功能特性

- ✅ 加载界面 + SVG 神经元动画
- ✅ Hero 区域 Canvas 神经网络动画
- ✅ 毛玻璃导航栏效果
- ✅ 3D 翻转信息卡片
- ✅ 文档系统（Markdown 渲染）
- ✅ 公告时间轴
- ✅ SSE 实时推送
- ✅ Admin 管理面板
- ✅ 极简密码鉴权

## Admin 访问

默认密码：`george2024`

访问 http://localhost:3000/admin/login

## 视觉风格

- 主色调：极深灰蓝 `#0D1117`
- 强调色：霓虹青 `#00FFCC` + 电音紫 `#B026FF`
- 字体：Fira Code (代码) + Inter (正文)
