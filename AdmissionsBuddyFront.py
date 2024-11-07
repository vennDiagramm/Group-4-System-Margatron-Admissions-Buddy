import AdmissionsBuddyBack as ABB

# Function to handle GUI
def main():
    # Streamlit set up
    ABB.st.set_page_config(page_title="Margatron", page_icon="Icons/mapua_icon_83e_icon.ico")
    ABB.st.title("Margatron, Admissions Buddy :books:")
    ABB.st.write("Hello, how may I help you?")

    # Provide the path to your database file here
    db_path = "database/databasefinalnjud.db"  # This is the SQLite database path
    ABB.handle_conversation(db_path)


# To run main   
if __name__ == "__main__":
    main()