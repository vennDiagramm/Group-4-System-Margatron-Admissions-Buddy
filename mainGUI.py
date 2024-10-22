import csv
import sqlite3 # for database
import google.generativeai as genai
import os
from pathlib import Path

# to deal with gui and secret keys
import streamlit as st
from dotenv import load_dotenv # comment out if diritso API_KEY from command line

# to deal with nonesense
import nonesenseChecking as nc

import re

# load the API KEY -- remove if command line
load_dotenv()

# Access the API_KEY environment variable
api_key = os.getenv('API_KEY')

# Configure the Gemini API using the API key from the environment variablee
genai.configure(api_key=api_key)
 

GREETING_KEYWORDS = ["hi", "hello", "hey", "greetings", "whats up", "what's up", "yo","how are you", "how are you doing"]
ACCEPTED_KEYWORDS = ["payment methods", "admissions", "requirements", "tuition fees", "enroll", "school year", "scholarships", "apply", "enrollment", "application", "pay", "departments", "colleges"]
GOODBYE_KEYWORDS = ["thank you", "goodbye", "farewell"]

# Connect to SQLite database and fetch the raw data
def extract_raw_data_from_db(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Fetch raw data (assuming it is stored as text in the database file)
    cursor.execute("SELECT * FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    if not tables:
        # Fetch raw content if no tables exist (assuming content is stored in the database file directly)
        with open(db_path, 'rb') as file:
            raw_data = file.read().decode('utf-8', errors='ignore')  # Decoding as UTF-8, modify if needed
        conn.close()
        return raw_data
    else:
        raise ValueError("The database contains tables, not raw data.")

    conn.close()


def remove_punctuation(text): #removes punctuations
    return re.sub(r'[^\w\s]', '', text)

def contains_keywords(user_input, keywords):
    user_input = remove_punctuation(user_input.lower())
    user_words = set(user_input.split())
    return bool(user_words.intersection(keywords))

# Use the Gemini API to generate a response based on the database content and user input
def query_gemini_api(db_path, user_input):
    # Gives out the tone the bot should respond
    tone = "Respond formally and professionally, providing only the requested information. Ensure the answer is clear and relevant to the query, without including any HTML tags and mentioning how the information was obtained. Provide links if needed."
    
    db_content = extract_raw_data_from_db(db_path)

    model = genai.GenerativeModel("gemini-1.5-flash")

    user_input = user_input.strip().lower()

    # If input matches accepted keywords
    if contains_keywords(user_input, ACCEPTED_KEYWORDS):
        response = model.generate_content([f"{tone}. Answer the following query based solely on the provided data: {user_input}. Limit the response to 500 words and omit unnecessary details.", db_content])
    elif contains_keywords(user_input, GOODBYE_KEYWORDS):
        return "You are very much welcome! I am glad I could help!"
    elif contains_keywords(user_input, GREETING_KEYWORDS):
        return "Hello! How can I assist you with admission information today?"

    # Nonsense input check
    elif (nc.is_mathematical_expression(user_input)) or (nc.is_nonsensical_input(user_input)):
        return "I'm sorry, I can't help you with that. Please ask questions regarding the admission process. Could you please ask something else or clarify your question?"

    else:
        response = model.generate_content([f"{tone}. Give me an answer based on this data and the query:  {user_input}. Limit up to 500 words", db_content])

    response = response.text

    if "Not found" in response or "Unavailable" in response or not response.strip():
        return "I'm sorry, I couldn't find an answer to your question. Could you please rephrase it or ask something else?" 
    
    return response

# Function to handle the conversation
def handle_conversation(csv_path):
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Capture user input -- mao kibali ni asa dapit mag chat c user. mao sab ni mo appear sa chatbox
    user_input = st.chat_input("Ask questions regarding admissions. Please be specific...")

    if user_input:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input}) 

        # Display user message in chat message container
        with st.chat_message("user"): # we can change this. this is the icon for the human
            st.markdown(user_input)

        # Query the Gemini API with the user input
        result =  query_gemini_api(db_path, user_input)

        # Display assistant response in chat message container
        with st.chat_message("assistant"): # icon for assistant
            st.markdown(result)

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": result})


# function to handle GUI
def main():
    # Streamlit set up
    st.set_page_config(page_title="Margatron", page_icon="Icons/mapua_icon_83e_icon.ico") # pwde nato e himo as mmcm logo
    st.title("Margatron, Admissions Buddy :books:")
    st.write("Hello, how may I help you?")

    # Provide the path to your CSV file here
    csv_path = "scrapped_FAQs.csv"
    handle_conversation(csv_path)


# to run main
if __name__ == "__main__":
    main()