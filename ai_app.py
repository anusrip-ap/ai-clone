import streamlit as st
from openai import OpenAI

st.title("Kimi Chatbot (NVIDIA NIM)")

# Initialize OpenAI Client pointing to NVIDIA NIM Base URL
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=st.secrets["NVIDIA_API_KEY"],
)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Process user input
if prompt := st.chat_input("Ask Kimi something..."):
    # Append user prompt to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Format the full message history for OpenAI chat completions
        formatted_messages = [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ]

        # Call the model via NVIDIA API
        completion = client.chat.completions.create(
            model="moonshotai/kimi-k2.6",  # Update to exact NVIDIA Kimi model ID if needed
            messages=formatted_messages,
            temperature=0.7,
        )

        response_text = completion.choices[0].message.content
        st.markdown(response_text)

    # Append assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response_text})
