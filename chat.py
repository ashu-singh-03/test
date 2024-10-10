from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Retrieve the API key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("API key is not set. Please ensure GOOGLE_API_KEY is in your .env file.")

genai.configure(api_key=api_key)

# Initialize chat with the Generative Model
chat = genai.GenerativeModel('gemini-pro')
history = []

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

# Initialize Streamlit app
st.set_page_config(page_title="Q&A Demo")
st.header("Gemini Application")

input_text = st.text_input("Input: ", key="input")
submit = st.button("Ask the question")

if submit:
    response = get_gemini_response(input_text)
    st.subheader("The Response is")
    for chunk in response:
        st.write(chunk.text)
        st.write("_" * 80)
    
    # Show chat history
    st.write(chat.history)
