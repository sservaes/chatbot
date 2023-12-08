import streamlit as st
from openai import OpenAI
import json

st.title("GPT-4 Chatbot")

# Open the file
with open("keys.json", "r") as f:
    keys = f.read()

# Load the JSON data into a dictionary
keys = json.loads(keys)

# Access OpenAI API key from the environment variable
client = OpenAI(
  api_key=keys["OPENAI_API_KEY"],
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
    
if prompt := st.chat_input("Enter your question here"):
    st.session_state["openai_model"] = "gpt-4-1106-preview"

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    messages = [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ]

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=messages,
            temperature=0.7,
            stream=True,
        ):
            full_response += (response.choices[0].delta.content or "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Button to clear the chat history
if len(st.session_state.messages) > 0:
    if st.button("Clear History"):
        st.session_state.messages = []
