import streamlit as st
from openai import OpenAI, APIError

st.title("Kimi Chatbot (NVIDIA NIM)")

# Initialize OpenAI Client with NVIDIA's base URL
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=st.secrets.get("NVIDIA_API_KEY"),
)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Process user input
if prompt := st.chat_input("Ask Kimi something..."):
    # Append user prompt to state
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Format messages for OpenAI compatibility
        formatted_messages = [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ]

        try:
            # NVIDIA Kimi K2.6 API Call
            completion = client.chat.completions.create(
                model="moonshotai/kimi-k2.6",
                messages=formatted_messages,
                temperature=0.7,
                max_tokens=4096,  # Required by NVIDIA NIM
            )

            response_text = completion.choices[0].message.content
            st.markdown(response_text)
            
            # Save assistant response
            st.session_state.messages.append({"role": "assistant", "content": response_text})

        except APIError as e:
            # This prints the precise reason NVIDIA rejected the request
            st.error(f"NVIDIA API Error ({e.status_code}): {e.message}")
        except Exception as e:
            st.error(f"Error: {e}")
