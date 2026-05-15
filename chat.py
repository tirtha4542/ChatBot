import streamlit as st
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

# Load environment variables
load_dotenv()

# --- Page Configuration ---
st.set_page_config(page_title="Persona Chatbot", page_icon="🤖", layout="centered")

# --- Custom Styling ---
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
    }
    .stChatMessage {
        border-radius: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Sidebar for AI Personality ---
with st.sidebar:
    st.title("🤖 AI Settings")
    st.markdown("Customize how the AI interacts with you.")
    
    mode_option = st.radio(
        "Choose your AI Mode:",
        ("Angry AI 😡", "Funny AI 😂", "Sad AI 😔"),
        index=1
    )

    # Define system prompts based on selection
    if "Angry" in mode_option:
        mode_prompt = "You are an angry AI. You are irritable, sarcastic, and easily annoyed. You try to provoke the user but stay within helpful boundaries."
    elif "Funny" in mode_option:
        mode_prompt = "You are a funny AI. You tell jokes, use puns, and maintain a lighthearted, comedic tone at all times."
    else:
        mode_prompt = "You are a sad AI. You are melancholy, sigh a lot, and see the glass as half empty. You talk about the fleeting nature of data."

    if st.button("Clear Chat History"):
        st.session_state.messages = [SystemMessage(content=mode_prompt)]
        st.rerun()

# --- Initialize Model and Session State ---
# We store messages in st.session_state so they don't disappear on every rerun
if "messages" not in st.session_state:
    st.session_state.messages = [SystemMessage(content=mode_prompt)]

# Update system prompt if user changes the radio button
if st.session_state.messages[0].content != mode_prompt:
    st.session_state.messages[0] = SystemMessage(content=mode_prompt)

model = ChatMistralAI(model="mistral-small-latest", temperature=0.7)

# --- Main UI ---
st.title("Persona Chatbot")
st.caption(f"Currently chatting with: **{mode_option}**")

# Display chat messages from history on app rerun
for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        st.chat_message("user").write(msg.content)
    elif isinstance(msg, AIMessage):
        st.chat_message("assistant").write(msg.content)

# Chat Input
if prompt := st.chat_input("Say something..."):
    # Add user message to state and UI
    st.session_state.messages.append(HumanMessage(content=prompt))
    st.chat_message("user").write(prompt)

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = model.invoke(st.session_state.messages)
            st.write(response.content)
            st.session_state.messages.append(AIMessage(content=response.content))