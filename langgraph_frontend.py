import streamlit as st

from langchain_ollama.chat_models import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from streamlit_js_eval import streamlit_js_eval

st.set_page_config(page_title="HR Interview Bot", page_icon="💼")
st.title("HR Interview Bot")

llm = ChatOllama(model="llama3.1:8b")

# ---------------- SETUP STATE ----------------
if "setup_complete" not in st.session_state:
    st.session_state.setup_complete = False
if 'user_message_count' not in st.session_state:
    st.session_state.user_message_count = 0
if 'feedback_shown' not in st.session_state:
    st.session_state.feedback_shown = False
if "messages" not in st.session_state:
        st.session_state.messages = []
if "chat_complete" not in st.session_state:
    st.session_state.chat_complete =False

def complete_setup():
    st.session_state.setup_complete = True
def show_feedback():
    st.session_state.feedback_shown = True

# ---------------- SETUP FORM ----------------
if not st.session_state.setup_complete:

    st.subheader("Personal Information", divider="rainbow")

    if "name" not in st.session_state:
        st.session_state.name = ""
    if "experience" not in st.session_state:
        st.session_state.experience = ""
    if "skills" not in st.session_state:
        st.session_state.skills = ""

    st.session_state.name = st.text_input(
        "Name", value=st.session_state.name, placeholder="Enter your name",max_chars=40
    )

    st.session_state.experience = st.text_area(
        "Experience", value=st.session_state.experience, placeholder="Enter your experience",max_chars=200
    )

    st.session_state.skills = st.text_area(
        "Skills", value=st.session_state.skills, placeholder="Enter your skills",max_chars=200
    )

    st.subheader("Company and Position", divider="rainbow")

    if "level" not in st.session_state:
        st.session_state.level = "Junior"
    if "position" not in st.session_state:
        st.session_state.position = "Data Scientist"
    if "company" not in st.session_state:
        st.session_state.company = "Amazon"

    col1, col2 = st.columns(2)

    with col1:
        st.session_state.level = st.radio(
            "Choose level",
            ["Junior", "Mid-level", "Senior"]
        )

    with col2:
        st.session_state.position = st.selectbox(
            "Choose position",
            ["Data Scientist", "Data Engineer", "ML Engineer", "BI Analyst", "Financial Analyst"]
        )

    st.session_state.company = st.selectbox(
        "Choose company",
        ["Amazon", "Meta", "Udemy", "365 Company", "Nestle"]
    )

    st.write(
        f"**Your information:** {st.session_state.level} "
        f"{st.session_state.position} at {st.session_state.company}"
    )

    # 🔥 MAIN FIX — SystemMessage created AFTER form submission
    if st.button("Start Interview"):
        st.session_state.messages = [
            SystemMessage(
                content=
                f"You are a HR executive interviewing {st.session_state.name}. "
                f"The candidate has experience: {st.session_state.experience} "
                f"and skills: {st.session_state.skills}. "
                f"You are interviewing them for the role of "
                f"{st.session_state.level} {st.session_state.position} "
                f"at {st.session_state.company}."
            )
        ]
        complete_setup()

# ---------------- CHAT STAGE ----------------
if st.session_state.setup_complete and not st.session_state.feedback_shown and not st.session_state.chat_complete:

    st.info("Start by introducing yourself.", icon="👋")
    if not st.session_state.messages:
        st.session_state.messages = [
        SystemMessage(
            content=
            f"You are a HR executive interviewing {st.session_state.name}. "
            f"The candidate has experience: {st.session_state.experience} "
            f"and skills: {st.session_state.skills}. "
            f"You are interviewing them for the role of "
            f"{st.session_state.level} {st.session_state.position} "
            f"at {st.session_state.company}."
        )
    ]

    # Display chat history
    for msg in st.session_state.messages:
        if isinstance(msg, HumanMessage):
            with st.chat_message("user"):
                st.markdown(msg.content)
        elif isinstance(msg, AIMessage):
            with st.chat_message("assistant"):
                st.markdown(msg.content)

    # Chat input
if st.session_state.user_message_count < 5:
    if prompt := st.chat_input("Your answer...",max_chars=1000):
        user_msg=HumanMessage(content=prompt)
        st.session_state['messages'].append(user_msg)
        with st.chat_message('user'):
            st.markdown(prompt)

        response=llm.invoke(st.session_state['messages'])
        st.session_state.messages.append(response)
        with st.chat_message('assistant'):
            st.markdown(response.content)

        st.session_state.user_message_count +=1

    if st.session_state.user_message_count >= 5:
        st.session_state.chat_complete = True

if st.session_state.chat_complete and not st.session_state.feedback_shown:
    if st.button("Get feedback"):
        st.write("Fetching feedback...")

if st.session_state.feedback_shown:
    st.subheader("Feedback")

    conversation_history = ""

    for msg in st.session_state.messages:
        if isinstance(msg, HumanMessage):
            conversation_history += f"Candidate: {msg.content}\n"
        elif isinstance(msg, AIMessage):
            conversation_history += f"Interviewer: {msg.content}\n"

    feedback_llm = ChatOllama(
        model="llama3.1:8b",
        temperature=0.3
    )

    feedback_prompt = [
        SystemMessage(
            content="""
    You are a helpful tool that provides feedback on an interviewee's performance.

    Before the feedback, give a score from 1 to 10.

    Follow this exact format:
    Overall Score: <number>
    Feedback: <your feedback>

    Give only the feedback.
    Do NOT ask any questions.
    Do NOT engage in conversation.
    """
        ),
        HumanMessage(
            content=f"""
    This is the interview you need to evaluate:

    {conversation_history}
    """
        )
    ]

    feedback_response = feedback_llm.invoke(feedback_prompt)
    st.write(feedback_response.content)
if st.button("Restart Interview", type="primary"):
    streamlit_js_eval(js_expressions="parent.window.location.reload()")