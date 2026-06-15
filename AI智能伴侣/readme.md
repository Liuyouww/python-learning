#项目：AI智能伴侣

一个基于Streamlit + DeepSeek API构建的长期陪伴型AI Companion项目。

支持：
- 多会话聊天
- AI自动生成会话标题
- 上下文连续对话
- 会话搜索
- 会话重命名
- 删除确认
- 重新生成回复
- 自定义伴侣姓名与性格
- 本地JSON持久化保存

#功能预览

##多会话聊天
每个会话对应一个独立AI伴侣聊天记录。
支持：
- 新建会话
- 历史会话切换
- 自动保存
- 会话搜索

##AI自动命名会话
用户第一次发言后，AI 自动生成：伴侣姓名_性格关键词_聊天主题
例如：小甜甜_温柔甜妹_深夜聊天
小峰_知心温暖_初次问候

##自定义伴侣
支持动态修改：伴侣姓名和性格设定
例如：小甜甜，温柔可爱小甜妹
系统 Prompt 会自动更新。

##重新生成回复
支持：
- 删除最新的assistant回复
- 保留用户消息
- 重新调用模型生成新回答

##本地会话持久化
所有聊天记录保存至：sessions/xxx.json
格式：
{
  "nick_name": "小甜甜",
  "nature": "温柔可爱小甜妹",
  "messages": [],
  "current_session": "小甜甜_温柔甜妹_深夜聊天"
}

#技术栈
- Python
- Streamlit
- OpenAI SDK
- DeepSeek API
- JSON 本地存储

#项目结构
AI智能伴侣/
│
├── app.py                 # Streamlit 主入口
├── ai_utils.py            # AI相关逻辑
├── session_utils.py       # 会话管理逻辑
│
├── sessions/              # 本地会话数据
│
├── requirements.txt       #简要写所调用库（非所有环境依赖）
└── README.md
