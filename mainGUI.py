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


GREETING_KEYWORDS = ["hi", "hello", "hey", "greetings", "whats up", "what's up", "yo"]
ACCEPTED_KEYWORDS = ["payment methods", "admissions", "requirements", "tuition fees", "enroll", "school year", "scholarships", "how to apply", "enrollment"]
GOODBYE_KEYWORDS = ["thank you", "goodbye", "farewell"]

# Function to extract text from CSV
def extract_text_from_csv(csv_path):
    csv_content = ""
    with open(csv_path, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            csv_content += ' '.join(row) + "\n"
    return csv_content

# Function to choose the appropriate CSV file based on user input
def select_csv_file(user_input):
    if "college" in user_input:
        return "admissionBot\scrapped_college.csv"
    elif "faq" in user_input or "question" in user_input:
        return "admissionBot\scrapped_FAQs.csv"
    elif "scholarship" in user_input:
        return "admissionBot\scrapped_scholarship.csv"
    else:
        return "admissionBot\scrapped_FAQs.csv"


# Use Gemini API to generate a response based on CSV content and user input
def query_gemini_api(user_input):
    # Set the bot's tone
    tone = "Respond in a formal and professional manner and give out any links if needed."
    
    # Select the CSV file based on the user input
    csv_path = select_csv_file(user_input)
    if csv_path is None:
        return "I'm sorry, I couldn't find any data related to your question."

    csv_content = extract_text_from_csv(csv_path)
    
    model = genai.GenerativeModel("gemini-1.5-flash")
    user_input = user_input.strip().lower()

    # Generate response based on input
    if any(phrase in user_input for phrase in ACCEPTED_KEYWORDS):
        response = model.generate_content([f"{tone}. Give me an answer based on this data and the query: {user_input}", csv_content])
    elif any(words in user_input for words in GOODBYE_KEYWORDS):
        return "You are very much welcome! I am glad I could help!"
    elif any(keyword in user_input for keyword in GREETING_KEYWORDS):
        return "Hello! How can I assist you with admission information today?" 
    elif (nc.is_mathematical_expression(user_input)) or (nc.is_nonsensical_input(user_input)):
        return "I'm sorry, I can't help you with that. Could you please ask something else or clarify your question?"
    else:
        response = model.generate_content([f"{tone}. Give me an answer based on this data and the query: {user_input}", csv_content])

    # Handle empty or unhelpful responses
    response = response.text
    if "Not found" in response or "Unavailable" in response or not response.strip():
        return "I'm sorry, I couldn't find an answer to your question. Could you please rephrase it or ask something else?" 
    return response


# Function to handle the conversation
def handle_conversation():
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
        result = query_gemini_api(user_input)

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
    st.write("Hello, how may I help you? Meow")

    # Provide the path to your CSV file here
    handle_conversation()


# to run main
if __name__ == "__main__":
    main()