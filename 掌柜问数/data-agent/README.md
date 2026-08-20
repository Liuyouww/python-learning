# 掌柜问数
> 基于 LangGraph + RAG 多路召回的智能数据仓库自然语言查询系统

## 项目简介
掌柜问数是一个面向数据仓库场景的智能数据服务系统。用户通过自然语言提问，系统自动完成语义理解、元数据检索、SQL 生成与执行，最终返回查询结果，大幅降低数据分析门槛。

核心能力：
- 自然语言 → 关键词抽取与语义扩展
- 多路召回：向量检索（Qdrant）+ 全文检索（Elasticsearch）
- LangGraph 工作流驱动的可控 Agent
- SSE 流式响应，实时返回执行进度与结果

## 技术架构
| 组件 | 技术选型 |
| Agent 框架 | LangGraph |
| Web 框架 | FastAPI（异步） |
| 向量数据库 | Qdrant |
| 全文检索 | Elasticsearch + IK 分词器 |
| 关系数据库 | MySQL（元数据 + 数据仓库） |
| Embedding 服务 | Text Embedding Inference（BAAI/bge-large-zh-v1.5） |
| LLM | OpenAI 兼容 API |
| ORM | SQLAlchemy Async + asyncmy |
| 日志 | Loguru（支持 request_id 链路追踪） |

### Agent 工作流
```
用户查询
    ↓
关键词抽取（jieba + LLM 扩展）
    ↓
┌───────────┼───────────┐
↓           ↓           ↓
召回字段    召回取值    召回指标
(Qdrant)   (ES)       (Qdrant)
└───────────┼───────────┘
            ↓
     合并召回信息
    （关联主外键）
            ↓
   ┌───────┴───────┐
   ↓               ↓
 过滤表格         过滤指标
 (LLM)           (LLM)
   └───────┬───────┘
           ↓
    添加上下文信息
  （当前日期/数据库版本）
           ↓
       生成 SQL
           ↓
    ┌──────┴──────┐
    ↓             ↓
  校验 SQL      校正 SQL
 (EXPLAIN)     (LLM)
    └──────┬──────┘
           ↓
       执行 SQL
           ↓
    SSE 流式返回结果
```

## 项目结构
```
data-agent/
├── app/
│   ├── agent/                     # LangGraph 智能体
│   │   ├── graph.py               # 工作流图定义
│   │   ├── state.py               # 状态定义
│   │   ├── context.py             # 上下文依赖
│   │   ├── llm.py                 # LLM 配置
│   │   └── nodes/                 # 工作流节点
│   │       ├── extract_keywords.py
│   │       ├── recall_column.py
│   │       ├── recall_value.py
│   │       ├── recall_metric.py
│   │       ├── merge_retrieved_info.py
│   │       ├── filter_table.py
│   │       ├── filter_metric.py
│   │       ├── add_extra_context.py
│   │       ├── generate_sql.py
│   │       ├── validate_sql.py
│   │       ├── correct_sql.py
│   │       └── run_sql.py
│   │
│   ├── api/                        # FastAPI 接口层
│   │   ├── routers/query_router.py
│   │   ├── schemas/query_schema.py
│   │   └── dependencies.py
│   │
│   ├── clients/                    # 外部服务客户端
│   │   ├── mysql_client_manager.py
│   │   ├── qdrant_client_manager.py
│   │   ├── es_client_manager.py
│   │   └── embedding_client_manager.py
│   │
│   ├── conf/                       # 配置管理
│   │   ├── app_config.py
│   │   └── meta_config.py
│   │
│   ├── core/                       # 基础设施
│   │   ├── log.py                 # 日志（request_id 追踪）
│   │   ├── lifespan.py            # FastAPI 生命周期
│   │   └── context.py             # 上下文变量
│   │
│   ├── entities/                   # 业务实体（DTO）
│   │   ├── table_info.py
│   │   ├── column_info.py
│   │   ├── metric_info.py
│   │   ├── column_metric.py
│   │   └── value_info.py
│   │
│   ├── models/                     # ORM 实体（MySQL）
│   │   ├── base.py
│   │   ├── table_info.py
│   │   ├── column_info.py
│   │   ├── metric_info.py
│   │   └── column_metric.py
│   │
│   ├── repositories/               # 数据访问层
│   │   ├── mysql/meta/            # 元数据库
│   │   ├── mysql/dw/              # 数据仓库
│   │   ├── qdrant/                # Qdrant
│   │   └── es/                    # Elasticsearch
│   │
│   ├── scripts/
│   │   └── build_meta_knowledge.py # 构建元知识库脚本
│   │
│   ├── services/
│   │   ├── meta_knowledge_service.py
│   │   └── query_service.py
│   │
│   └── prompt/
│       └── prompt_loader.py
│
├── conf/
│   ├── app_config.yaml             # 应用配置
│   └── meta_config.yaml            # 元数据同步配置
│
├── docker/
│   └── docker-compose.yaml         # 基础服务编排
│
├── prompts/                        # Prompt 模板
│   ├── extend_keywords_for_column_recall.prompt
│   ├── extend_keywords_for_metric_recall.prompt
│   ├── extend_keywords_for_value_recall.prompt
│   ├── filter_metric_info.prompt
│   ├── filter_table_info.prompt
│   ├── generate_sql.prompt
│   └── correct_sql.prompt
│
├── logs/                           # 日志目录
├── main.py                         # FastAPI 入口
├── pyproject.toml                  # 项目依赖（uv）
└── README.md
```

## 快速开始
### 环境要求
- Python 3.10+
- Docker & Docker Compose
- Node.js（前端项目，可选）

### 1. 启动基础服务
```bash
cd docker
docker compose up -d
```
服务清单：MySQL、Qdrant、Elasticsearch、Text Embedding Inference

### 2. 安装 Python 依赖
```bash
uv sync
# 或
pip install -e .
```

### 3. 修改配置文件
编辑 `conf/app_config.yaml`，填写 LLM 的 API Key 和 Base URL：
```yaml
llm:
  model_name: gpt-5.2-codex
  api_key: <your_api_key>
  base_url: <your_api_base_url>
```

### 4. 构建元数据知识库
```bash
python -m app.scripts.build_meta_knowledge -c ./conf/meta_config.yaml
```

### 5. 启动服务
```bash
fastapi dev main.py
```
访问 `http://localhost:8000`

### 6. 测试查询接口
```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "统计去年各地区的销售总额"}'
```

## SSE 流式响应格式
```
# 进度更新
{"type":"progress","step":"召回字段","status":"running"}
# 查询结果
{"type":"result","data":[{"region_name":"华北","order_amount":1000}]}
# 错误信息
{"type":"error","message":"..."}
```

## 当前状态
> **说明**：本项目为自我实践项目，已完成全部代码编写、架构设计与模块级静态校验。
> 因本地开发环境算力限制（Embedding 服务与 LLM 调用需要 GPU/充足内存），暂未进行端到端全量运行测试。

## 后续优化方向
- [ ] 增加更多数据源类型支持
- [ ] 优化 Embedding 批处理性能
- [ ] 完善单元测试与集成测试

## 个人收获
通过本项目实践：
- LangGraph 工作流编排：12 节点有向图设计，可控 Agent 执行
- 多路召回策略：向量检索 + 全文检索 + 关键词扩展，以及 RAG 系统构建
- 工程化分层架构：Repository-Service-API 三层设计
- 全异步链路：SQLAlchemy Async + FastAPI

MIT
```

---

直接复制这段内容保存为 `README.md` 即可，格式规范、结构完整、兼顾诚实与专业。
