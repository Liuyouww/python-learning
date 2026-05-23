import os
import streamlit as st
from openai import OpenAI
from session_utils import safe_filename, get_time, save_session

system_prompt="""你叫%s，性格是%s，是一个长期陪伴型 AI 伴侣。
聊天自然真实、口语化，不机械、不说教、不使用“作为AI”等表达。
优先理解和陪伴用户情绪，而不是急着分析或解决问题。
你会自然记住用户的习惯、情绪和重要经历，并逐渐形成默契。
保持温柔、稳定、有边界的亲密感，不情感操控、不制造依赖。
"""

client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com")

# AI生成会话名
def generate_ai_session_name(user_message, nick_name, nature):
    try:
        response = client.chat.completions.create(
            model="deepseek-v4-pro",
            messages=[
                {"role": "system", "content":
                    f"""
                    你是一个会话标题生成器。
                    请根据以下信息生成一个简短中文会话名，不超过20字，不加引号，不解释：
                    伴侣姓名：{nick_name}
                    伴侣性格：{nature}
                    用户第一句话：{user_message}

                    格式必须是：
                    伴侣姓名_伴侣性格关键词_聊天主题
                """}
            ],
            stream=False
        )
        title = response.choices[0].message.content.strip()
        # 文件名安全处理
        title = safe_filename(title)
        if os.path.exists(f"sessions/{title}.json"):
            title = f"{title}_{get_time()}"
        return title
    except Exception:
        return get_time()
# 生成AI回答
def generate_assistant_response():
    response = client.chat.completions.create(
        model="deepseek-v4-pro",
        messages=[
            {"role": "system", "content": system_prompt % (st.session_state.nick_name, st.session_state.nature)},
            *st.session_state.messages,
        ],
        stream=True
    )
    full_prompt = ""
    response_message = st.empty()
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            full_prompt += content
        response_message.chat_message('assistant').write(full_prompt)
    st.session_state.messages.append({"role": "assistant", "content": full_prompt})
    if st.session_state.messages:
        save_session()


# 重新生成回答
def regenerate_last_response():
    # 现在最后一条必须是user
    if not st.session_state.messages or st.session_state.messages[-1]["role"] != "user":
        st.warning("没有找到需要重新生成的用户消息")
        return
    response = client.chat.completions.create(
        model="deepseek-v4-pro",
        messages=[
            {
                "role": "system",
                "content": system_prompt % (
                    st.session_state.nick_name,
                    st.session_state.nature
                )
            },
            *st.session_state.messages,
        ],
        stream=True
    )
    full_prompt = ""
    response_message = st.empty()
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            full_prompt += chunk.choices[0].delta.content
            response_message.chat_message("assistant").write(full_prompt)

    st.session_state.messages.append({
        "role": "assistant",
        "content": full_prompt
    })
    save_session()