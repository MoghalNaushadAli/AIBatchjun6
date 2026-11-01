import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

load_dotenv()

st.title("GPT Chat")
st.write("Ask GPT a question and continue the conversation.")

st.caption("Powered by OpenAI's gpt-4o-mini model.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Let's start chatting! 👇"}
    ]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.error(
            "OPENAI_API_KEY is not set. Add it to the .env file, then restart the app."
        )
        st.stop()

    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        try:
            stream = OpenAI(api_key=api_key).chat.completions.create(
                model="gpt-4o-mini",
                messages=st.session_state.messages,
                stream=True,
            )
            for chunk in stream:
                token = chunk.choices[0].delta.content or ""
                full_response += token
                message_placeholder.markdown(full_response + "▌")
        except OpenAIError as error:
            st.error(f"OpenAI request failed: {error}")
        else:
            message_placeholder.markdown(full_response)
            st.session_state.messages.append(
                {"role": "assistant", "content": full_response}
            )
