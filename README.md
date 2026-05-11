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

### 前端开发

```bash
cd frontend
npm install
npm run dev
```

访问 http://localhost:3000

### 后端开发

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

## Nginx 部署

项目根目录的 `nginx.conf` 是 Linux/macOS 下的反向代理配置。

### 前置条件

1. 安装 nginx
2. 打包前端：`cd frontend && npm run build`
3. 后端运行在 `http://127.0.0.1:8000`

### 部署步骤

```bash
# 1. 将前端 dist 目录复制到 web 目录
sudo cp -r frontend/dist /var/www/geek-site/

# 2. 复制 nginx 配置
sudo cp nginx.conf /etc/nginx/sites-available/geek-site

# 3. 编辑配置，修改 server_name 为你的域名或 IP
sudo nano /etc/nginx/sites-available/geek-site

# 4. 启用站点
sudo ln -s /etc/nginx/sites-available/geek-site /etc/nginx/sites-enabled/

# 5. 测试配置
sudo nginx -t

# 6. 重载 nginx
sudo systemctl reload nginx

# 7. 启动后端（后台运行）
cd backend
nohup python run.py > backend.log 2>&1 &
```

### 配置说明

| 配置项 | 说明 |
|--------|------|
| `/` | 前端静态文件（dist 目录） |
| `/api` | 反向代理到后端 `127.0.0.1:8000` |
| `/assets` | 静态资源，缓存 30 天 |
| `/health` | 健康检查端点 |

### HTTPS 配置（可选）

```nginx
server {
    listen 443 ssl;
    server_name your_domain;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    # ... 其他配置同 nginx.conf
}
```
