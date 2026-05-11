import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import engine, Base, SessionLocal
from app.models import Document, Announcement
from datetime import datetime


def init_database():
    print("正在创建数据库表...")
    Base.metadata.create_all(bind=engine)
    print("数据库表创建完成！")


def seed_data():
    db = SessionLocal()
    
    existing_docs = db.query(Document).count()
    if existing_docs > 0:
        print("数据库已有数据，跳过初始化...")
        db.close()
        return
    
    print("正在添加示例数据...")
    
    docs = [
        Document(
            title="欢迎访问我的极客空间",
            slug="welcome",
            content="""# 欢迎访问我的极客空间 👋

很高兴你能来到这里！这是我用来分享技术见解、记录学习历程的个人网站。

## 关于这个网站

这是一个使用 **Vue 3** + **FastAPI** 构建的现代化个人网站，旨在展示：

- 📝 技术博客与学习笔记
- 📚 API 文档与开发指南
- 🔔 网站动态与更新通知

## 技术栈

本网站的构建涉及以下技术：

```javascript
// 前端
const frontend = ['Vue 3', 'Vite', 'Tailwind CSS', 'Pinia']

// 后端
const backend = ['FastAPI', 'SQLAlchemy', 'SQLite']

// 工具
const tools = ['Git', 'Docker', 'GitHub Actions']
```

## 联系我

如果你有任何问题或建议，欢迎通过以下方式联系我：

- GitHub: [github.com/george](https://github.com)
- Email: george@example.com
""",
            category="blog",
            tags=["欢迎", "关于"],
            order_index=0
        ),
        Document(
            title="Python FastAPI 快速入门",
            slug="fastapi-quickstart",
            content="""# Python FastAPI 快速入门

FastAPI 是一个现代、快速（高性能）的 Python Web 框架，基于标准 Python 类型提示。

## 安装

```bash
pip install fastapi uvicorn
```

## 第一个 API

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}
```

## 运行服务器

```bash
uvicorn main:app --reload
```

## 文档自动生成

FastAPI 会自动为你生成 API 文档：

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 下一步

- [x] 基础路由
- [ ] 请求体与响应模型
- [ ] 数据库集成
- [ ] 认证与授权
""",
            category="docs",
            tags=["Python", "FastAPI", "教程"],
            order_index=1
        ),
        Document(
            title="Vue 3 Composition API 指南",
            slug="vue3-composition-api",
            content="""# Vue 3 Composition API 指南

Composition API 是 Vue 3 引入的一种新的编写组件逻辑的方式。

## 为什么使用 Composition API？

1. **更好的逻辑复用** - 通过 composables 实现逻辑共享
2. **更灵活的代码组织** - 相关逻辑可以放在一起
3. **更好的 TypeScript 支持** - 与类型系统无缝集成

## 基本用法

```vue
<script setup>
import { ref, computed, onMounted } from 'vue'

const count = ref(0)
const doubled = computed(() => count.value * 2)

const increment = () => {
  count.value++
}

onMounted(() => {
  console.log('组件已挂载')
})
</script>
```

## Composables

Composable 是封装和复用有状态逻辑的函数：

```javascript
// useCounter.js
import { ref } from 'vue'

export function useCounter() {
  const count = ref(0)
  
  const increment = () => count.value++
  const decrement = () => count.value--
  
  return { count, increment, decrement }
}
```

## 生命周期钩子

```javascript
import { onMounted, onUpdated, onUnmounted } from 'vue'

onMounted(() => {
  // 组件挂载后
})

onUpdated(() => {
  // 组件更新后
})

onUnmounted(() => {
  // 组件卸载后
})
```
""",
            category="docs",
            tags=["Vue 3", "JavaScript", "前端"],
            order_index=2
        ),
        Document(
            title="机器学习基础概念",
            slug="ml-basics",
            content="""# 机器学习基础概念

机器学习是人工智能的一个分支，它使计算机能够从数据中学习并做出预测。

## 监督学习 vs 无监督学习

### 监督学习

使用标记数据进行训练：

| 算法 | 用途 |
|------|------|
| 线性回归 | 预测连续值 |
| 逻辑回归 | 二分类 |
| 决策树 | 分类/回归 |
| 随机森林 | 集成学习 |

### 无监督学习

从未标记数据中发现模式：

- **聚类**: K-Means, DBSCAN
- **降维**: PCA, t-SNE
- **关联规则**: Apriori

## 模型评估指标

```python
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# 分类指标
accuracy = accuracy_score(y_true, y_pred)
precision = precision_score(y_true, y_pred)
recall = recall_score(y_true, y_pred)
f1 = f1_score(y_true, y_pred)
```

## 过拟合与欠拟合

- **过拟合**: 模型在训练数据上表现良好，但在新数据上表现差
- **欠拟合**: 模型在训练和新数据上都表现不佳

### 解决方案

| 问题 | 解决方法 |
|------|----------|
| 过拟合 | 正则化、交叉验证、增加数据 |
| 欠拟合 | 增加模型复杂度、添加特征 |
""",
            category="blog",
            tags=["机器学习", "AI", "数据科学"],
            order_index=3
        )
    ]
    
    announcements = [
        Announcement(
            title="网站正式上线",
            content="欢迎访问我的个人极客空间！这里将持续更新技术博客、文档教程以及项目动态。",
            type="success",
            priority=100
        ),
        Announcement(
            title="新增文档搜索功能",
            content="文档页面现在支持实时搜索，可以快速找到你需要的文章内容。",
            type="info",
            priority=90
        ),
        Announcement(
            title="网站维护通知",
            content="计划于本周六凌晨进行系统升级，预计 downtime 为 30 分钟。",
            type="warning",
            priority=80
        ),
        Announcement(
            title="新增博客分类",
            content="博客新增了标签系统，可以按主题快速筛选相关文章。",
            type="info",
            priority=70
        )
    ]
    
    for doc in docs:
        db.add(doc)
    
    for ann in announcements:
        db.add(ann)
    
    db.commit()
    db.close()
    print("示例数据添加完成！")


if __name__ == "__main__":
    init_database()
    seed_data()
    print("数据库初始化完成！")
