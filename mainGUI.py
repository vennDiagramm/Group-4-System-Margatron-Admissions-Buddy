import csv
import google.generativeai as genai
import os
from pathlib import Path

# to deal with gui and secret keys
import streamlit as st
from dotenv import load_dotenv # comment out if diritso API_KEY from command line

# to deal with nonesense
import re
from nltk.corpus import words


# load the API KEY -- remove if command line
load_dotenv()

# Access the API_KEY environment variable
api_key = os.getenv('API_KEY')

# Configure the Gemini API using the API key from the environment variable
genai.configure(api_key=api_key)

# Extract data from a CSV file
def extract_text_from_csv(csv_path):
    csv_content = ""
    with open(csv_path, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            # Convert each row to a string and append to the content
            csv_content += ' '.join(row) + "\n"
    return csv_content

# Checking if gibberish like asdsacaewefhj
def is_nonsensical_input(user_input):
    # Check if the input consists of gibberish or random letters
    if re.match(r'^[a-z]+$', user_input) and len(user_input) > 5:
        return True

    # Check if the input contains too many consecutive consonants or vowels
    if re.search(r'(?i)([bcdfghjklmnpqrstvwxyz]{4,}|[aeiou]{4,})', user_input):
        return True

    # Check if the input is not in the dictionary of valid words
    valid_words = set(words.words())  # Load valid words
    input_words = user_input.split()
    if all(word not in valid_words for word in input_words):
        return True

    return False

# Checking if math ba siya
def is_mathematical_expression(user_input):
    # Check if the input is a mathematical expression
    return re.match(r'^[\d\s\+\-\*\/\%\(\)]+$', user_input.strip()) is not None

# Use the Gemini API to generate a response based on the CSV content and user input
def query_gemini_api(csv_path, user_input):
    csv_content = extract_text_from_csv(csv_path)
    
    model = genai.GenerativeModel("gemini-1.5-flash")

    user_input = user_input.strip().lower()
    
    if user_input in ["hi", "hello", "hey", "greetings"]:
        return "Hello! How can I assist you with admission information today?"
    # Nonsense input check 
    elif is_mathematical_expression(user_input) or is_nonsensical_input(user_input):
        return "I'm sorry, I can't help you with that. Could you please ask something else or clarify your question?"
    else:
        response = model.generate_content([f"Give me an answer based on this data and the query: {user_input}", csv_content])
    
    response = response.text

    if "Not found" in response or "Unavailable" in response or not response.strip():
        return "I'm sorry, I couldn't find an answer to your question. Could you please rephrase it or ask something else?" 
    
    return response  # Assuming the API returns the text in this field

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
        result = query_gemini_api(csv_path, user_input)

        # Display assistant response in chat message container
        with st.chat_message("assistant"): # icon for assistant
            st.markdown(result)

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": result})


# function to handle GUI
def main():
    # Streamlit set up
    st.set_page_config(page_title="Margatron", page_icon="🤖") # pwde nato e himo as mmcm logo
    st.title("Margatron, Admissions Buddy :books:")
    st.write("Hello, how may I help you?")

    # Provide the path to your CSV file here
    csv_path = "scrapped_data1.csv"
    handle_conversation(csv_path)


# to run main
if __name__ == "__main__":
    main()