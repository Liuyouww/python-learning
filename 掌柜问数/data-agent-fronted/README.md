# 掌柜问数 - 前端交互界面
> 基于 Vue 3 + Vite 构建的智能数据查询交互界面，支持 SSE 流式响应与实时进度展示

## 项目简介
本项目是「掌柜问数」智能数据仓库查询系统的**前端交互界面**，为业务人员提供自然语言查询入口，并与后端 Agent 服务通过 SSE（Server-Sent Events）协议通信，实时展示查询执行进度与结果。

核心功能：
- 自然语言查询输入
- 实时展示 Agent 工作流执行进度（关键词抽取 → 召回 → 过滤 → SQL 生成 → 执行）
- 查询结果表格化展示
- 错误信息友好提示

## 技术栈

| 类别 | 技术 |
|------|------|
| 框架 | Vue 3（Composition API） |
| 构建工具 | Vite |
| 开发语言 | TypeScript |
| 状态管理 | Pinia（如使用） |
| HTTP 通信 | EventSource（SSE 原生协议） |
| UI 组件库 | （按实际使用填写，如 Element Plus / Ant Design Vue / 原生） |

## 项目结构
```
data-agent-fronted/
├── src/
│   ├── api/                 # API 接口层（SSE 连接）
│   │   └── query.js        # 查询接口封装
│   ├── components/          # 公共组件
│   │   ├── QueryInput.vue  # 查询输入框
│   │   ├── ProgressBar.vue # 进度展示组件
│   │   └── ResultTable.vue # 结果表格展示
│   ├── views/               # 页面视图
│   │   └── Home.vue        # 主页面
│   ├── stores/              # Pinia 状态管理（如使用）
│   ├── utils/               # 工具函数
│   ├── App.vue              # 根组件
│   └── main.ts              # 入口文件
├── index.html
├── package.json
├── vite.config.ts
└── README.md
```

## 快速开始
### 环境要求
- Node.js 16+
- npm / pnpm / yarn

### 安装依赖
```bash
npm install
# 或
pnpm install
```

### 开发环境启动
```bash
npm run dev
```
访问 `http://localhost:5173`

### 生产环境构建
```bash
npm run build
```

### 预览生产构建
```bash
npm run preview
```


## 页面功能
| 区域 | 功能说明 |
|------|----------|
| **查询输入框** | 用户输入自然语言问题（如“统计去年各地区的销售总额”） |
| **进度追踪区** | 实时显示 Agent 各节点执行状态（running / success / error） |
| **结果展示区** | 以表格形式展示查询结果数据 |
| **错误提示** | 当查询失败时，显示友好的错误信息 |


## 与后端对接
前端通过 **SSE（Server-Sent Events）** 协议与后端 FastAPI 服务通信：

```javascript
// 示例：建立 SSE 连接
const eventSource = new EventSource('/api/query-stream?query=统计销售额')
eventSource.onmessage = (event) => {
  const data = JSON.parse(event.data)
  // 处理进度更新 / 结果返回 / 错误信息
}
```

后端 API 地址配置在 `.env` 环境变量中：

```
VITE_API_BASE_URL=http://localhost:8000
```


## 当前状态
> **说明**：本项目为课程实践的配套前端界面，已完成页面布局、组件设计与 API 对接逻辑编写。
> 因后端服务（Agent 与相关基础设施）暂未完成端到端部署，目前处于**界面静态展示与逻辑代码完成阶段**，待后端服务就绪后可快速完成联调。
---

把这段内容保存为 `data-agent-fronted/README.md`，你的两个项目（后端 + 前端）就都有了规范的展示页面。

**小提示**：如果你简历里同时放了前后端两个 GitHub 链接，记得在前端 README 里加一句“配套后端项目：[后端仓库地址]”，在后台 README 里也对应加上“配套前端项目：[前端仓库地址]”，形成完整的项目矩阵，面试官印象分会更高。🍻
