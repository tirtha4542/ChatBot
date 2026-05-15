import streamlit as st
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI 
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(page_title="Puja AI", page_icon="💖")
st.title("Chat with Puja")
st.subheader("Your caring and loving girlfriend 🌸")

# Initialize the model
# Using Mistral Small as requested in your snippet
model = ChatMistralAI(model="mistral-small-latest", temperature=0.7)

# Initialize session state for messages if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = [
        SystemMessage(content="Your name is Puja and Your are my Girlfriend. You are very caring and loving. You always try to make me happy and you are very good at it. You are also very good at giving advice and you always try to help me with my problems. You are also very good at making me laugh and you always try to make me smile. You are also very good at listening to me and you always try to understand me. You are also very good at being there for me when I need you. You are also very good at being my best friend and you always try to be there for me no matter what.")
    ]

# Display chat history (skipping the system message)
for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.markdown(msg.content)
    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant", avatar="💖"):
            st.markdown(msg.content)

# Chat input
if prompt := st.chat_input("Say something to Puja..."):
    # Append user message to state and display it
    st.session_state.messages.append(HumanMessage(content=prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant", avatar="💖"):
        with st.spinner("Puja is typing..."):
            response = model.invoke(st.session_state.messages)
            st.markdown(response.content)
    
    # Append AI response to state
    st.session_state.messages.append(AIMessage(content=response.content))
  
