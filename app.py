import streamlit as st
from text2text import OpenAIClient
from get_file_contents import PythonFileReader
import logging

logging.basicConfig(level=logging.INFO)

st.title("GPT-4 32K App")

# Create an instance of the OpenAIClient class.
openai_client = OpenAIClient()

# Initialize session state for conversation history.
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = [("You are a coding assistant that writes production quality code.", 'system')]

# Input text area for user prompt.
user_input = st.text_area("Enter your prompt:")

# Additional optional input for local path.
local_path = st.text_input("Enter a local path (optional):")

if local_path:
    # Get an instance of the PythonFileReader class.
    file_reader = PythonFileReader(local_path)
    file_contents = file_reader.get_files_content()
    # Append files content to the conversation history as user messages.
    st.session_state.conversation_history += [(content, 'user') for content in file_contents]

if st.button("Generate Response"):
    if user_input:
        response = openai_client.get_response(user_input, st.session_state.conversation_history)
        st.markdown(f"**Response:** \n{response}")

st.info("This is a Streamlit app for interacting with Azure OpenAI.")