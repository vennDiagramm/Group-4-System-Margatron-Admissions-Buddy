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


# Keywords for conversation
GREETING_KEYWORDS = ["hi", "hello", "hey", "greetings", "whats up", "what's up", "yo", "how are you", "how are you doing"]
ACCEPTED_KEYWORDS = ["payment methods", "admissions", "requirements", "tuition fees", "enroll", "school year", "scholarships", "apply", "enrollment", "application", "pay", "departments", "colleges", "SHS", "JHS", "College programs", "courses", "junior high school", "senior high school"]
GOODBYE_KEYWORDS = ["thank you", "goodbye", "farewell"]
TABLE_KEYWORDS = {
    # Admissions-related keywords
    "admissions": "ADMISSION",
    "faqs": "ADMISSION",
    "jhs": "ADMISSION",
    "shs": "ADMISSION",
    
    # ATYCB-related keywords
    "accountancy": "ATYCB",
    "entrepreneurship": "ATYCB",
    "real estate": "ATYCB",
    "management accounting": "ATYCB",
    "tourism": "ATYCB",
    
    # CAS-related keywords
    "multimedia arts": "CAS",
    "communication": "CAS",
    
    # CCIS-related keywords
    "computer science": "CCIS",
    "information systems": "CCIS",
    "emc": "CCIS",  
    
    # CEA-related keywords
    "architecture": "CEA",
    "chemical engineering": "CEA",
    "electronic engineering": "CEA",
    "civil engineering": "CEA",
    "environmental engineering": "CEA",
    "mechanical engineering": "CEA",
    "ce": "CEA",  
    "me": "CEA", 
    
    # CHS-related keywords
    "psychology": "CHS",
    "pharmacy": "CHS",
    "physical therapy": "CHS",
    "bio": "CHS",  
}

# Connect to SQLite database and fetch the raw data from a specific table || we can create in separte class file
def extract_raw_data_from_db(db_path, table_name):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Use the table_name parameter in the SQL query
    query = f"SELECT content FROM {table_name}"  # Adjust this line to select the specific column
    cursor.execute(query)  
    rows = cursor.fetchall()

    # Joining the rows as a string for the API input
    db_content = "\n".join([row[0] for row in rows])  # Assuming 'content' is the first column
    
    conn.close()
    return db_content


# Remove punctuations || this one either rename nonsenseChecker or create a class file for this one and contains_keywords
def remove_punctuation(text):  # removes punctuations
    return re.sub(r'[^\w\s]', '', text)


# Check if user input contains any keywords || same class file above
def contains_keywords(user_input, keywords):
    user_input = remove_punctuation(user_input.lower())
    user_words = set(user_input.split())
    return bool(user_words.intersection(keywords))


# query handler
def query_gemini_api(db_path, user_input):
    # Tone for the bot's response
    tone = "Respond formally and professionally, providing only the requested information. Ensure the answer is clear and relevant to the query, without including any HTML tags and mentioning how the information was obtained. Provide links if needed."
    
    # Default table
    table_to_query = "all_data"

    # Check for specific keywords to switch tables
    for keyword, table in TABLE_KEYWORDS.items():
        if keyword in user_input.lower():
            table_to_query = table
            break

    # Extracting the content from the specified table
    db_content = extract_raw_data_from_db(db_path, table_to_query)

    # Load the Gemini model
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Clean the user input
    user_input = user_input.strip().lower()

    # If input matches accepted keywords
    if contains_keywords(user_input, ACCEPTED_KEYWORDS):
        response = model.generate_content([f"{tone}. Answer the following query based solely on the provided data: {user_input}. Limit the response to 500 words and omit unnecessary details.", db_content])
    
    # If user is saying goodbye
    elif contains_keywords(user_input, GOODBYE_KEYWORDS):
        return "You are very much welcome! I am glad I could help!"
    
    # If user is greeting the bot
    elif contains_keywords(user_input, GREETING_KEYWORDS):
        return "Hello! How can I assist you with admission information today?"

    # Nonsense input check
    elif (nc.is_mathematical_expression(user_input)) or (nc.is_nonsensical_input(user_input)):
        return "I'm sorry, I can't help you with that. Please ask questions regarding the admission process. Could you please ask something else or clarify your question?"

    # Keywords sa table
    if contains_keywords(user_input, TABLE_KEYWORDS.keys()):
        response = model.generate_content([f"{tone}. Answer the following query based solely on the provided data: {user_input}. Limit the response to 500 words and omit unnecessary details.", db_content])

    # For general queries
    else:
        response = model.generate_content([f"{tone}. Give me an answer based on this data and the query: {user_input}. Limit up to 500 words", db_content])

    # Extract the response text
    response = response.text

    # If the response is not valid
    if "Not found" in response or "Unavailable" in response or not response.strip():
        return "I'm sorry, I couldn't find an answer to your question. Could you please rephrase it or ask something else?" 
    
    return response


# Function to handle the conversation
def handle_conversation(db_path):
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        # para unsa mani ???? ||| hi gais, notice me
        avatar_path = 'https://raw.githubusercontent.com/vennDiagramm/admissionBot/refs/heads/main/Icons/student.ico' if message["role"] == "user" else 'https://raw.githubusercontent.com/vennDiagramm/admissionBot/refs/heads/main/Icons/mapua_icon_83e_icon.ico'
        
        with st.chat_message(message["role"], avatar=avatar_path):
            st.markdown(message["content"])

    # Capture user input -- mao kibali ni asa dapit mag chat c user. mao sab ni mo appear sa chatbox
    user_input = st.chat_input("Ask questions regarding admissions. Please be specific...")

    if user_input:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input}) 

        # Display user message in chat message container
        user_avatar = 'https://raw.githubusercontent.com/vennDiagramm/admissionBot/refs/heads/main/Icons/student.ico'
        with st.chat_message("user", avatar = user_avatar):  # we can change this. this is the icon for the human
            st.markdown(user_input)

        # Query the Gemini API with the user input
        result = query_gemini_api(db_path, user_input)

        # Display assistant response in chat message container
        assistant_avatar = 'https://raw.githubusercontent.com/vennDiagramm/admissionBot/refs/heads/main/Icons/mapua_icon_83e_icon.ico'
        with st.chat_message("assistant", avatar = assistant_avatar):  # icon for assistant
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
    db_path = "databasefinal.db"  # This is the SQLite database path
    handle_conversation(db_path)


if __name__ == "__main__":
    main()
