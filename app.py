import os
import uuid
from dotenv import load_dotenv
import streamlit as st
import chromadb
from google.generativeai import configure, generate_text  # Adjust this based on the method found

# Load environment variables from the .env file
load_dotenv()

# Retrieve the API key from the environment variable
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("API key is not set. Please ensure GOOGLE_API_KEY is in your .env file.")

# Configure the Google API with the retrieved API key
configure(api_key=api_key)

# Initialize the Chroma client
client = chromadb.Client()

# Create or get the chat history collection
collection_name = "chat_history"
try:
    collection = client.create_collection(name=collection_name)
    st.success(f"Collection '{collection_name}' created successfully.")
except Exception as e:
    if "already exists" in str(e):
        collection = client.get_collection(name=collection_name)
        st.info(f"Collection '{collection_name}' already exists. Using the existing collection.")
    else:
        st.error(f"Error creating collection: {e}")
        collection = None

# Streamlit app layout
st.title("Chat Application")

# Function to get a response from the Gemini API
def get_gemini_response(user_input):
    try:
        # Ensure user_input is valid
        if not user_input:
            return "No input provided."

        # Call the API to generate a response
        response = generate_text(prompt=user_input)

        # Check the structure of the response to ensure you're accessing it correctly
        if hasattr(response, 'text'):
            return response.text  # Return the generated text
        else:
            return "Received unexpected response structure."

    except Exception as e:
        # Log the error for debugging
        st.error(f"Error retrieving response from Gemini API: {e}")
        return "I'm sorry, I couldn't get a response."

# Input text box for user messages
user_input = st.text_input("You: ", "")

if st.button("Send"):
    if user_input:
        unique_id = str(uuid.uuid4())
        collection.add(documents=[user_input], ids=[unique_id])
        
        # Get a response from the Gemini API
        response = get_gemini_response(user_input)
        
        # Display the response
        st.write(f"Gemini: {response}")
    else:
        st.warning("Please enter a message before sending.")
