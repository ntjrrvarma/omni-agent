import streamlit as st
import requests
import os

# Set page config for a professional look
st.set_page_config(page_title="Omni-Agent | SRE Copilot", page_icon="🤖", layout="centered")

st.title("🛡️ Omni-Agent Enterprise Copilot")
st.caption("Powered by LangChain, FastAPI, Qdrant, and PostgreSQL")

# Get backend URL from environment, default to localhost for local dev
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# Initialize chat history in Streamlit session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello Engineer. I am your SRE Copilot. I can query live telemetry or search compliance manuals. How can I assist?"}
    ]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
user_query = st.chat_input("Ask about server status, freezers, or SOPs...")

if user_query:
    # 1. Display user message in chat message container
    st.chat_message("user").markdown(user_query)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_query})

    # 2. Send query to our FastAPI Backend
    with st.spinner("Omni-Agent is thinking and routing your request..."):
        try:
            # Use backend service name in Docker
            response = requests.post(
                f"{BACKEND_URL}/ask", 
                json={"question": user_query}
            )
            
            if response.status_code == 200:
                answer = response.json().get("answer", "No answer found.")
            else:
                answer = f"⚠️ API Error: {response.status_code}"
                
        except Exception as e:
            answer = f"⚠️ Connection Error: Is the FastAPI backend running? ({str(e)})"

    # 3. Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(answer)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": answer})