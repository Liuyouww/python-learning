#项目：Multi-Session AI Assistant

基于Streamlit + DeepSeek API构建的多会话AI助手系统。

支持：
- 多会话聊天
- 角色设定
- AI自动生成会话标题
- 会话搜索
- 会话重命名
- 删除确认
- 重新生成回复
- 本地JSON持久化保存

#功能预览

##多会话聊天
每个会话对应一个独立AI助手聊天记录。
支持：
- 新建会话
- 历史会话切换
- 自动保存
- 会话搜索

##AI自动命名会话
用户第一次发言后，AI 自动生成：助手名称_角色设定关键词_聊天主题
例如：AI助手_专业耐心_查找文献

##助手设定
支持动态修改：助手名称和角色设定
例如：AI助手，专业、耐心的学习助手
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
  "assistant_name": "AI助手",
  "assistant_role": "专业、耐心的学习助手",
  "messages": [],
  "current_session": "AI助手_专业耐心_查找文献"
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
