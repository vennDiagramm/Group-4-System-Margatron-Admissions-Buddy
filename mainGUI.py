import csv
import sqlite3  # for database
import google.generativeai as genai
import os
from pathlib import Path

# to deal with gui and secret keys
import streamlit as st
from dotenv import load_dotenv  # comment out if directly using API_KEY from command line

# to deal with nonsense inputs
import nonesenseChecking as nc

import re

# load the API KEY -- remove if command line
load_dotenv()

# Access the API_KEY environment variable
api_key = os.getenv('API_KEY')

# Configure the Gemini API using the API key from the environment variable
genai.configure(api_key=api_key)


# Keywords for conversation || FACTS
GREETING_KEYWORDS = ["hi", "hello", "hey", "greetings", "whats up", "what's up", "yo", "how are you", "how are you doing"]
ACCEPTED_KEYWORDS = ["payment methods", "admissions", "requirements", "tuition fees", "enroll", "school year", "scholarships", 
                     "apply", "enrollment", "application", "pay", "departments", "colleges", "shs", "jhs", "college programs", 
                     "courses", "junior high school", "senior high school", "ccis", "cea","atycb","cas","chs", "college"]
GOODBYE_KEYWORDS = ["thank you", "goodbye", "farewell"]

# Connect to SQLite database and fetch the raw data
def extract_raw_data_from_db(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT * from DataBase")  
    rows = cursor.fetchall()

    # Joining the rows as a string for the API input
    db_content = "\n".join([" ".join(map(str, row)) for row in rows])
    
    conn.close()
    return db_content


# Remove punctuations
def remove_punctuation(text):  # removes punctuations
    return re.sub(r'[^\w\s]', '', text)


# Check if user input contains any keywords
def contains_keywords(user_input, keywords):
    user_input = remove_punctuation(user_input.lower())
    user_words = set(user_input.split())
    return bool(user_words.intersection(keywords))

def is_greeting(user_input):
    """Check if the user input contains any greeting keyword."""
    return contains_keywords(user_input, GREETING_KEYWORDS)

def is_accepted_query(user_input):
    """Check if the user input contains any accepted keyword related to admissions."""
    return contains_keywords(user_input, ACCEPTED_KEYWORDS)

def is_goodbye(user_input):
    """Check if the user input contains any goodbye keyword."""
    return contains_keywords(user_input, GOODBYE_KEYWORDS)

# Define logic rules for handling responses
def chatbot_logic(user_input):
    """
    Logic-based response system for the chatbot.
    Instead of sequential if-else, we check for multiple conditions (rules).
    """
    if is_greeting(user_input):
        return "Hello! How can I assist you with admission information today?"
    
    elif is_goodbye(user_input):
        return "You are very much welcome! I am glad I could help!"

    elif is_accepted_query(user_input):
        return "Sure, I can help with that. Please provide more specific details regarding your query."

    # Default case if no rule applies
    return "I'm sorry, I didn't quite understand. Could you please rephrase your question?"


def query_gemini_api(db_path, user_input):
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Process user input with logic programming style
    result = chatbot_logic(user_input)
    
    if result:
        return result
    
    tone = "Respond formally and professionally..."
    db_content = extract_raw_data_from_db(db_path)

    try:
        response = model.generate_content([f"{tone}. Give me an answer based on this data and the query: {user_input}. Limit up to 500 words", db_content])
        response_text = response.text if hasattr(response, 'text') else ""
        
        # Handle invalid or empty responses more specifically
        if "Not found" in response_text or "Unavailable" in response_text or not response_text.strip():
            print("Response contained 'Not found' or 'Unavailable' or was empty.")
            return "I'm sorry, I couldn't find an answer to your question. Could you please rephrase it or ask something else?"
        
        return response_text
    
    except Exception as e:
        print(f"Error generating response: {e}")
        return "I'm sorry, there was an error processing your request. Please try again later."




# Function to handle the conversation
def handle_conversation(db_path):
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        avatar_path = 'https://raw.githubusercontent.com/vennDiagramm/admissionBot/refs/heads/main/Icons/student.ico' if message["role"] == "user" else 'https://raw.githubusercontent.com/vennDiagramm/admissionBot/refs/heads/main/Icons/mapua_icon_83e_icon.ico'
        
        with st.chat_message(message["role"], avatar=avatar_path):
            st.markdown(message["content"])

    # Capture user input -- mao kibali ni asa dapit mag chat c user. mao sab ni mo appear sa chatbox
    user_input = st.chat_input("Ask questions regarding admissions. Please be specific...")

    if user_input:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input}) 

        # Display user message in chat message container
        with st.chat_message("user", avatar = 'https://raw.githubusercontent.com/vennDiagramm/admissionBot/refs/heads/main/Icons/student.ico'):  # we can change this. this is the icon for the human
            st.markdown(user_input)

        # Query the Gemini API with the user input
        result = query_gemini_api(db_path, user_input)

        # Display assistant response in chat message container
        with st.chat_message("assistant", avatar = 'https://raw.githubusercontent.com/vennDiagramm/admissionBot/refs/heads/main/Icons/mapua_icon_83e_icon.ico'):  # icon for assistant
            st.markdown(result)

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": result})


# Function to handle GUI
def main():
    # Streamlit set up
    st.set_page_config(page_title="Margatron", page_icon="Icons/mapua_icon_83e_icon.ico")  # pwde nato e himo as mmcm logo
    st.title("Margatron, Admissions Buddy :books:")
    st.write("Hello, how may I help you?")

    # Provide the path to your database file here
    db_path = "database/database5.db"  # This is the SQLite database path
    handle_conversation(db_path)


# To run main   
if __name__ == "__main__":
    main()
