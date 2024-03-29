import streamlit as st
import cohere

with st.sidebar:
    API_KEY = st.text_input("Cohere API Key", key="chatbot_api_key", type="password")
    "[Get an Cohere API key](https://cohere.com/)"
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

st.title("💬 Chatbot")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "CHATBOT", "message": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["message"])

prompt = st.chat_input()
if prompt:
    if not API_KEY:
        st.info("Please add your Cohere API key to continue.")
        st.stop()

    client = cohere.Client(API_KEY)
    st.chat_message("USER").write(prompt)
    response = client.chat(chat_history=st.session_state.messages, message=prompt)
    st.session_state.messages.append({"role": "USER", "message": prompt})
    msg = response.text
    st.session_state.messages.append({"role": "CHATBOT", "message": msg})
    st.chat_message("CHATBOT").write(msg)