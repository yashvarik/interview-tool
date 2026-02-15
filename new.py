import streamlit as st
from langchain_ollama.chat_models import ChatOllama
from langchain_core.messages import SystemMessage,HumanMessage,AIMessage
llm=ChatOllama(model='llama3.1:8b')

if 'setup_complete' not in st.session_state:
    st.session_state['setup_complete'] = False

if 'messages' not in st.session_state:
    st.session_state['messages']=[]


    def setup():
        st.session_state['setup_complete'] = True

if not st.session_state['setup_complete']:
    st.subheader('Chatbot')
    if 'name' not in st.session_state:
        st.session_state['name']=[]
    if 'experience' not in st.session_state:
        st.session_state['experience']=[]
    if 'skills' not in st.session_state:
        st.session_state['skills']=[]

    st.session_state['name']=st.text_input(label="Enter your name",value=st.session_state.name,placeholder="Enter your name")
    st.session_state['experience']=st.text_input(label='Enter your experience',value=st.session_state.experience,placeholder="Enter your experience")
    st.session_state['skills']=st.text_area(label='Enter your skills',value=st.session_state.skills,placeholder="Enter your skills")
    st.write(f"your name{st.session_state['name']}")
    st.write(f"your experience{st.session_state['experience']}")
    st.write(f"your skills{st.session_state['skills']}")




