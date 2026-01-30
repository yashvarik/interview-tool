import streamlit as st
from langchain_ollama.chat_models import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
if 'setup_complete' not in st.session_state:
    st.session_state['setup_complete'] = False

def setup_complete():
    st.session_state.setup_complete = True

if not st.session_state.setup_complete:
    st.subheader('Your personal information',divider='rainbow')
    if 'name' not in st.session_state:
        st.session_state['name'] =''
    if 'experience' not in st.session_state:
        st.session_state['experience'] =''
    if 'skills' not in st.session_state:
        st.session_state['skills']=''

st.session_state.name=st.text_input(label='Name',value=st.session_state['name'],max_chars=None,placeholder='Please enter your name')
st.session_state.experience=st.text_area(label='Experience',value=st.session_state['experience'],max_chars=None,placeholder='Please enter your experience')
st.session_state.skills=st.text_area(label='skills',value=st.session_state['skills'],max_chars=None,placeholder='Please enter your skills')

if 'level' not in st.session_state:
    st.session_state['level']='junior'
if 'position' not in st.session_state:
    st.session_state['position'] ='Data Scientist'
if 'company' not in st.session_state:
    st.session_state['company']='Amazon'

col1,col2=st.columns(2)
with col1:
    st.session_state.level=st.radio(
        'choose your level',
        ['junior','medium','senior']
    )

with col2:
    st.session_state.position=st.selectbox(
      'choose your position',
        ['Data Scientist','Data Engineer','Data Scientist','ML Engineer','IT Manager']
    )
st.session_state.company=st.selectbox(
    'choose your company',
    ['Facebook','Amazon','Apple','netflix','Google']
)
st.header('Your filled details')
st.write(f"your name: {st.session_state['name']}")
st.write(f"your experience: {st.session_state['experience']}")
st.write(f"your skills: {st.session_state['skills']}")
st.write(f"your level: {st.session_state['level']}")
st.write(f"your position: {st.session_state['position']}")
st.write(f"your company: {st.session_state['company']}")

    if st.button('Start interview'):

        st.session_state['messsages']=[
        SystemMessage(content=
                f"You are a HR executive interviewing {st.session_state.name}. "
                f"The candidate has experience: {st.session_state.experience} "
                f"and skills: {st.session_state.skills}. "
                f"You are interviewing them for the role of "
                f"{st.session_state.level} {st.session_state.position} "
                f"at {st.session_state.company}.")
    ]
    setup_complete()

if st.session_state.setup_complete:
    st.info("Start by introducing yourself.", icon="👋")






if 'messages' not in st.session_state:
    st.session_state['messages'] =[]
for msg in st.session_state['messages']:
    if isinstance(msg,SystemMessage):
     continue
    elif isinstance(msg,HumanMessage):
        with st.chat_message('user'):
            st.markdown(msg.content)
    elif isinstance(msg,AIMessage):
        with st.chat_message('assistant'):
            st.markdown(msg.content)


llm=ChatOllama(model='llama3.1:8b')

if prompt:=st.chat_input():
    user_msg=HumanMessage(content=prompt)
    st.session_state['messages'].append(user_msg)
    with st.chat_message('user'):
         st.markdown(prompt)

    response=llm.invoke(st.session_state['messages'])
    st.session_state['messages'].append(response)
    with st.chat_message('assistant'):
        st.markdown(response.content)



