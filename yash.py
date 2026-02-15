from langchain_classic.chains.constitutional_ai.prompts import examples
from langchain_ollama.chat_models import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import streamlit as st

llm = ChatOllama(model="llama3.1:8b")

st.subheader("Chatbot", divider="rainbow")

# ---------------- SESSION STATE ---------------- #

if "messages" not in st.session_state:
    st.session_state.messages = []

if "setup_complete" not in st.session_state:
    st.session_state.setup_complete = False

if "name" not in st.session_state:
    st.session_state.name = ""

if "skills" not in st.session_state:
    st.session_state.skills = ""

if "experience" not in st.session_state:
    st.session_state.experience = ""


# ---------------- USER INFO INPUT ---------------- #

if not st.session_state.setup_complete:

    st.session_state.name = st.text_input(
        "Enter your name",
        value=st.session_state.name
    )

    st.session_state.skills = st.text_area(
        "Enter your skills",
        value=st.session_state.skills
    )

    st.session_state.experience = st.text_area(
        "Enter your experience",
        value=st.session_state.experience
    )

    if st.button("Start Interview"):
        st.session_state.setup_complete = True
        st.session_state.messages = []  # reset chat


# ---------------- BUILD SYSTEM PROMPT DYNAMICALLY ---------------- #

def build_system_prompt():
    return SystemMessage(
        content=(
            f"You are a helpful career assistant. "
            f"Address the user by name: {st.session_state.name}. "
            f"Suggest job roles based on skills: {st.session_state.skills}. "
            f"Experience: {st.session_state.experience}. "
            f"If skills are lacking, suggest improvements. "
            f"Always end with 3 related follow-up questions."
        )
    )


# ---------------- SHOW CHAT HISTORY ---------------- #

for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.markdown(msg.content)
    elif isinstance(msg, AIMessage):
        with st.chat_message("ai"):
            st.markdown(msg.content)


# ---------------- CHAT INPUT ---------------- #

if st.session_state.setup_complete:

    if prompt := st.chat_input("Ask your career question..."):

        user_msg = HumanMessage(content=prompt)
        st.session_state.messages.append(user_msg)

        with st.chat_message("user"):
            st.markdown(prompt)

        # 🔥 Important: fresh system prompt inject karo
        messages_for_llm = [build_system_prompt()] + st.session_state.messages

        response = llm.invoke(messages_for_llm)

        st.session_state.messages.append(response)

        with st.chat_message("ai"):
            st.markdown(response.content)