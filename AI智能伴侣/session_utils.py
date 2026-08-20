import os
import streamlit as st
from datetime import datetime
import json

# 防止生成系统非法文件名
def safe_filename(name):
    illegal_chars = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
    for char in illegal_chars:
        name = name.replace(char, '_')
    return name.strip()
# 生成会话名
def get_time():
    return datetime.now().strftime('%Y-%m-%d %H_%M_%S')
# 保存会话信息
def save_session():
    if st.session_state.current_session:
        session_data = {"nick_name": st.session_state.nick_name,
                        "nature": st.session_state.nature,
                        "messages": st.session_state.messages,
                        "current_session": st.session_state.current_session}
        if not os.path.exists('sessions'):
            os.mkdir('sessions')
        with open(f'sessions/{st.session_state.current_session}.json', 'w', encoding='utf-8') as f:
            json.dump(session_data, f, ensure_ascii=False, indent=2)
# 获取会话列表
def get_sessions_list():
    sessions_list= []
    if os.path.exists('sessions'):
        for session in os.listdir('sessions'):
            if session.endswith('.json'):
                sessions_list.append(session[:-5])
    sessions_list.sort(reverse=True)
    return sessions_list

# 加载显示指定会话内容
def load_session(session_name):
    try:
        if os.path.exists(f'sessions/{session_name}.json'):
            with open(f'sessions/{session_name}.json', 'r', encoding='utf-8') as f:
                session_data = json.load(f)
                st.session_state.nick_name = session_data['nick_name']
                st.session_state.nature = session_data['nature']
                st.session_state.messages = session_data['messages']
                st.session_state.current_session = session_name
    except Exception:
        st.error('加载会话失败!')
# 删除指定会话
def delete_session(session_name):
    try:
        if os.path.exists(f'sessions/{session_name}.json'):
            os.remove(f'sessions/{session_name}.json')
            if session_name==st.session_state.current_session:
                st.session_state.messages=[]
                st.session_state.current_session='新会话'
    except Exception:
        st.error('删除会话失败!')
# 会话重命名
def rename_session(old_name, new_name):
    try:
        new_name = safe_filename(new_name)

        if not new_name:
            st.error("会话名不能为空")
            return

        old_path = f"sessions/{old_name}.json"
        new_path = f"sessions/{new_name}.json"

        if not os.path.exists(old_path):
            st.error("原会话不存在")
            return

        if os.path.exists(new_path):
            st.error("这个会话名已经存在")
            return

        os.rename(old_path, new_path)

        if st.session_state.current_session == old_name:
            st.session_state.current_session = new_name

            with open(new_path, 'r', encoding='utf-8') as f:
                session_data = json.load(f)

            session_data["current_session"] = new_name

            with open(new_path, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, ensure_ascii=False, indent=2)

    except Exception:
        st.error("重命名失败")