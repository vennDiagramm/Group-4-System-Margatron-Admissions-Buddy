import csv
import google.generativeai as genai
import os
from pathlib import Path

# to deal with gui and secret keys
import streamlit as st
from dotenv import load_dotenv # comment out if diritso API_KEY from command line

# to deal with nonesense
import nonesenseChecking as nc


# load the API KEY -- remove if command line
load_dotenv()

# Access the API_KEY environment variable
api_key = os.getenv('API_KEY')

# Configure the Gemini API using the API key from the environment variable
genai.configure(api_key=api_key)

# Define constants
TONE = "Respond in a formal and professional manner and give out any links if needed. Do not say anything about reading from a text."
GREETING_KEYWORDS = ["hi", "hello", "hey", "greetings", "whats up", "what's up", "yo"]
ACCEPTED_PHRASES = ["payment methods", "admissions", "requirements", "tuition fees", "enroll", "school year", "scholarships"]
GOODBYE_WORDS = ["thank you", "goodbye", "farewell"]



# Extract data from a CSV file
def extract_text_from_csv(csv_path):
    try:
        csv_content = ""
        with open(csv_path, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                csv_content += ' '.join(row) + "\n"
        return csv_content
    except FileNotFoundError:
        st.error("CSV file not found. Please ensure the correct file path.")
        return ""
    except Exception as e:
        st.error(f"An error occurred while reading the CSV file: {str(e)}")
        return ""

 # Use the Gemini API to generate a response based on the CSV content and user input
def query_gemini_api(csv_path, user_input):
    user_input = user_input.strip().lower()
    csv_content = extract_text_from_csv(csv_path)
    
    if not csv_content:
        return "Error: CSV data could not be loaded."
    
    if any(phrase in user_input for phrase in ACCEPTED_PHRASES):
        query = f"{TONE}. Give me an answer based on this data and the query: {user_input}"
    elif any(word in user_input for word in GOODBYE_WORDS):
        return "You are very much welcome! I am glad I could help!"
    elif any(keyword in user_input for keyword in GREETING_KEYWORDS):
        return "Hello! How can I assist you with admission information today?"
    elif nc.is_mathematical_expression(user_input) or nc.is_nonsensical_input(user_input):
        return "I'm sorry, I can't help you with that. Could you please ask something else or clarify your question?"
    else:
        query = f"{TONE}. Give me an answer based on this data and the query: {user_input}"

    response = model.generate_content([query, csv_content]).text

    if "Not found" in response or "Unavailable" in response or not response.strip():
        return "I'm sorry, I couldn't find an answer to your question. Could you please rephrase it or ask something else?"
    
    return response



# Function to handle the conversation
def handle_conversation(csv_path):
    if "messages" not in st.session_state:
        st.session_state.messages = []

    user_input = st.chat_input("Ask specific questions about admissions, scholarships, and school requirements...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        
        result = query_gemini_api(csv_path, user_input)
        with st.chat_message("assistant"):
            st.markdown(result)

        st.session_state.messages.append({"role": "assistant", "content": result})



# function to handle GUI
def main():
    # Streamlit set up
    st.set_page_config(page_title="Margatron", page_icon="🤖") # pwde nato e himo as mmcm logo
    st.title("Margatron, Admissions Buddy :books:")
    st.write("Hello, how may I help you?")

    # Provide the path to your CSV file here
    csv_path = "scrapped_scholarship.csv"
    handle_conversation(csv_path)


# to run main
if __name__ == "__main__":
    main()