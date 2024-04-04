import os
import requests
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize environment variables
LANGUAGE_MODEL_API_KEY = os.getenv('LANGUAGE_MODEL_API_KEY')
LANGUAGE_MODEL_URL = f"https://generativelanguage.googleapis.com/v1beta1/models/chat-bison-001:generateMessage?key={LANGUAGE_MODEL_API_KEY}"

# Define the function to get the response from the language model API
def get_language_model_response(text):
    payload = {
        "prompt": { "messages": [{ "content": text }] },
        "temperature": 0.1,
        "candidate_count": 1,
    }
    headers = {"Content-Type": "application/json"}
    
    response = requests.post(LANGUAGE_MODEL_URL, json=payload, headers=headers)
    
    if response.status_code == 200:
        response_data = response.json()
        content = response_data['candidates'][0]['content']
        return content
    else:
        raise Exception(f"Error from language model API: {response.status_code}, {response.text}")

# Custom CSS to inject contained in a string
custom_css = """
<style>
    .stTextInput>div>div>input {
        color: white;
        background-color: #4E2A84;
        border-radius: 20px;
        border: 1px solid #4E2A84;
        padding: 10px;
    }
    .stButton>button {
        color: white;
        background-color: #4A90E2;
        border-radius: 20px;
        border: none;
        padding: 10px 24px;
        margin: 10px 0;
    }
    .message-bubble {
        padding: 10px 20px;
        background-color: #262730;
        border-radius: 30px;
        color: white;
        max-width: 60%;
        margin: 10px auto;
        word-wrap: break-word;
        border: 1px solid #4E2A84;
    }
    .st-bb {
        background-color: transparent;
    }
    .st-at {
        background-color: #0E1117;
    }
    .css-2trqyj {
        background-color: #0E1117;
    }
    .css-xq1lnh-EmotionIconBase {
        color: #F63366;
    }
</style>
"""

# Inject custom CSS with Markdown
st.markdown(custom_css, unsafe_allow_html=True)

# Layout and style of the app
st.title('InkoChat Bot 🤖')

st.title('AI Conversation using PaLM 2 🧠')

st.markdown("""
This app utilizes a powerful language model to engage in conversation. 
Type your message below and receive an AI-generated response.
""")

# Input text box with some styling
user_input = st.text_input("Enter your query here...", max_chars=200)

# When the 'Ask me ...' button is pressed, make the API call and display the response
if st.button('Ask me ...', help='Click to send your message to the AI'):
    if user_input:
        with st.spinner('AI is generating a response...'):
            try:
                response_content = get_language_model_response(user_input)
                # Display the response in a styled message bubble
                st.markdown(f'<div class="message-bubble">{response_content}</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(str(e))
    else:
        st.warning('Please enter some text to send.')

# Add details about the model or API below
st.info('This interface connects to a state-of-the-art language model API that generates contextual responses.')
