# for database and api
import sqlite3 
import google.generativeai as genai
import os

# to deal with gui and secret keys
import streamlit as st
from dotenv import load_dotenv

# to deal with nonsense inputs
import nonesenseChecking as nc

# for streamlit -- because mawala sa iyaha si words
import nltk
nltk.download('words')

# load the API KEY -- remove if command line
load_dotenv()

# Access the API_KEY environment variable
api_key = os.getenv('API_KEY')

# Configure the Gemini API using the API key from the environment variable
genai.configure(api_key=api_key)

# Create an instance of InputChecker
input_checker = nc.InputChecker()

# Keywords for conversation || FACTS - Lists
GREETING_KEYWORDS = ["hi", "hello", "hey", "greetings", "whats up", "what's up", "yo", "how are you", "how are you doing"]
ACCEPTED_KEYWORDS = ["payment methods", "admissions", "requirements", "tuition fees", "enroll", "school year", "scholarships", 
                     "apply", "enrollment", "application", "pay", "departments", "colleges", "shs", "jhs", "college programs", 
                     "courses", "junior high school", "senior high school", "ccis", "cea","atycb","cas","chs", "college", 
                     "senior high school", "junior high school","mmcm","mcm"]
GOODBYE_KEYWORDS = ["thank you", "goodbye", "farewell", "thanks", "ty", "thank", "bye"]


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


# Check if user input contains any keywords
def contains_keywords(user_input, keywords):
    user_input = input_checker.remove_punctuation(user_input.lower())
    user_words = set(user_input.split())
    return bool(user_words.intersection(keywords))


# Use the Gemini API to generate a response based on the database content and user input
def query_gemini_api(db_path, user_input):
    # Gives out the tone the bot should respond
    tone = "Respond formally and professionally, providing only the requested information. Ensure the answer is clear and relevant to the query, without including any HTML tags and mentioning how the information was obtained. Provide links if needed."
    
    # Extracting the content from the database
    db_content = extract_raw_data_from_db(db_path)

    # Load the Gemini model # gemini-1.5-flash / models/gemini-1.5-pro / models/gemini-1.0-pro -- different Gemini Models
    model = genai.GenerativeModel("models/gemini-1.5-flash-8b")

    # Clean the user input
    user_input = user_input.strip().lower()

    # If input matches accepted keywords
    if contains_keywords(user_input, ACCEPTED_KEYWORDS):
        response = model.generate_content([f"{tone}. Give me an answer based on this data and the query: {user_input}. Limit up to 500 words", db_content])
    
    # If user is saying goodbye
    elif contains_keywords(user_input, GOODBYE_KEYWORDS):
        return "You are very much welcome! I am glad I could help!"
    
    # If user is greeting the bot
    elif contains_keywords(user_input, GREETING_KEYWORDS) and len(user_input) <= 17:
        return "Hello! How can I assist you with admission information today?"
    
    # Nonsense input check
    elif any([input_checker.is_mathematical_expression(user_input), input_checker.is_nonsensical_input(user_input)]):
        return "I'm sorry, I can't help you with that. Please ask questions regarding the admission process. Could you please ask something else or clarify your question?"


    # For general queries
    else:
        response = model.generate_content([f"{tone}. Search from and Give me an answer based on this data and the query: {user_input}. Limit up to 500 words", db_content])

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
        avatar_path = 'https://raw.githubusercontent.com/vennDiagramm/admissionBot/refs/heads/main/Icons/student.ico' if message["role"] == "user" else 'https://raw.githubusercontent.com/vennDiagramm/admissionBot/refs/heads/main/Icons/mapua_icon_83e_icon.ico'
        
        with st.chat_message(message["role"], avatar=avatar_path):
            st.markdown(message["content"])

    # Capture user input -- mao kibali ni asa dapit mag chat c user. mao sab ni mo appear sa chatbox
    user_input = st.chat_input("Ask questions regarding admissions. Please be specific...")

    if user_input:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input}) 

        # Display user message in chat message container
        with st.chat_message("user", avatar = 'https://raw.githubusercontent.com/vennDiagramm/admissionBot/refs/heads/main/Icons/student.ico'):  # icon for the human
            st.markdown(user_input)

        # Query the Gemini API with the user input
        result = query_gemini_api(db_path, user_input)

        # Display assistant response in chat message container
        with st.chat_message("assistant", avatar = 'https://raw.githubusercontent.com/vennDiagramm/admissionBot/refs/heads/main/Icons/mapua_icon_83e_icon.ico'):  # icon for assistant
            st.markdown(result)

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": result})