import streamlit as st
from datetime import datetime

from session_utils import (
    save_session,
    get_sessions_list,
    load_session,
    delete_session,
    rename_session
)

from ai_utils import (
    generate_ai_session_name,
    generate_assistant_response,
    regenerate_last_response
)

st.markdown("""
<style>
section[data-testid="stSidebar"] h1 {
    margin-top: -1rem;
}
</style>
""", unsafe_allow_html=True)

st.set_page_config(page_title='AI智能伴侣',page_icon='🤖',layout='wide',initial_sidebar_state='expanded')


#初始化保存信息
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'nick_name' not in st.session_state:
    st.session_state.nick_name = '小甜甜'
if 'nature' not in st.session_state:
    st.session_state.nature = '温柔可爱小甜妹'
if 'current_session' not in st.session_state:
    st.session_state.current_session = '新会话'
if "menu_session" not in st.session_state:
    st.session_state.menu_session = None
if "rename_session" not in st.session_state:
    st.session_state.rename_session = None
if "delete_session" not in st.session_state:
    st.session_state.delete_session = None
if "regenerating" not in st.session_state:
    st.session_state.regenerating = False

st.text(f'更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}')
for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])

if st.session_state.regenerating:
    regenerate_last_response()
    st.session_state.regenerating = False
    st.rerun()

with st.sidebar:
    st.title('AI智能伴侣')
    if st.button('新建会话',icon='✏️',width='stretch'):
        # 1.保存当前会话
        save_session()
        # 2.新建新的会话
        if st.session_state.messages:
            st.session_state.messages = []
            st.session_state.current_session = '新会话'
            st.rerun()
            if st.session_state.messages:
                save_session()

    st.subheader("当前会话操作")
    if st.button("🔄 重新生成上一条回复", width="stretch"):
        if not st.session_state.messages:
            st.warning("当前没有可重新生成的内容")
        if (
                st.session_state.messages
                and st.session_state.messages[-1]["role"] == "assistant"
        ):
            st.session_state.messages.pop()
        st.session_state.regenerating = True
        save_session()
        st.rerun()

    # 分割线
    st.divider()

    st.header('伴侣信息')
    nick_name = st.text_input('姓名', placeholder=f'{st.session_state.nick_name}')
    if nick_name:
        st.session_state.nick_name = nick_name
    nature = st.text_area('性格（初始设置：温柔可爱小甜妹）', placeholder=f'{st.session_state.nature}')
    if nature:
        st.session_state.nature = nature

    st.divider()

    st.subheader('历史会话')
    sessions_list = get_sessions_list()

    # 会话搜索框
    find_name=st.text_input('搜索会话',placeholder='请输入伴侣姓名、性格或主题')
    if find_name:
        sessions_list=[session for session in sessions_list if find_name.lower() in session.lower()]
    if not sessions_list:
        st.info('没有找到匹配的会话')
    for session in sessions_list:
        col1, col2 = st.columns([6, 1])
        with col1:
            if st.button(
                    session,
                    width='stretch',
                    key=f'load_{session}',
                    type='primary' if session == st.session_state.current_session else 'secondary'
            ):
                load_session(session)
                st.rerun()
        with col2:
            if st.button(
                    '⋮',
                    width='stretch',
                    key=f'menu_{session}'
            ):
                if st.session_state.menu_session == session:
                    st.session_state.menu_session = None
                else:
                    st.session_state.menu_session = session
                st.rerun()

        # 显示小菜单
        if st.session_state.menu_session == session:
            if st.button('重命名',width='stretch',key=f'rename_{session}'):
                st.session_state.rename_session = session
                st.session_state.menu_session = None
                st.rerun()
            if st.button('删除',width='stretch',key=f'delete_{session}'):
                st.session_state.delete_session = session
                st.session_state.menu_session = None
                st.rerun()
        # 显示重命名输入
        if st.session_state.rename_session == session:
            new_name=st.text_input('',value=session,key=f'rename_input_{session}')
            subcol1,subcol2=st.columns(2)
            with subcol1:
                if st.button('',icon='✔️',width='stretch',key=f'save_rename_{session}'):
                    rename_session(session,new_name)
                    st.session_state.rename_session = None
                    st.rerun()
            with subcol2:
                if st.button('',icon='✖️',width='stretch',key=f'cancel_rename_{session}'):
                    st.session_state.rename_session = None
                    st.rerun()
        # 显示删除确认
        if st.session_state.delete_session == session:
            st.warning(f'确定删除会话：{session}吗？')
            del_col1,del_col2=st.columns(2)
            with del_col1:
                if st.button('确认',width='stretch',key=f'confirm_delete_{session}'):
                    delete_session(session)
                    st.session_state.delete_session = None
                    st.rerun()
            with del_col2:
                if st.button('取消',width='stretch',key=f'cancel_delete_{session}'):
                    st.session_state.delete_session = None
                    st.rerun()


need_rerun = False

prompt=st.chat_input('请输入您的问题')
if prompt:
    st.chat_message('user').write(prompt)
    st.session_state.messages.append({"role":"user","content":prompt})
    if st.session_state.current_session == "新会话":
        ai_title = generate_ai_session_name(
            prompt,
            st.session_state.nick_name,
            st.session_state.nature
        )
        st.session_state.current_session = ai_title
        need_rerun=True
    generate_assistant_response()
    if need_rerun:
        st.rerun()
