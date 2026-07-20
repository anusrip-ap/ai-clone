import streamlit as st
from google import genai

st.title("Kimi Chatbot")

# Initialize Gemini Client using Streamlit secret
client = genai.Client(api_key=st.secrets["KIMI_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Process user input
if prompt := st.chat_input("Ask Gemini something..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # UPDATED: Changed model to "gemini-2.0-flash"
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )
        st.markdown(response.text)

    st.session_state.messages.append({"role": "assistant", "content": response.text})
