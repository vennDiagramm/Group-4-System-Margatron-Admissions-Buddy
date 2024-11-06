# Admission Chatbot for Mapúa Malayan Colleges Mindanao

Welcome to the repository for our Admission Chatbot project, developed as part of our CS121 course, Programming Languages. This web-hosted GUI application is designed to assist prospective students with their admission queries and provide a user-friendly experience.

## Technologies Used

- **Python**: The primary programming language for implementing the chatbot’s logic and functionality.
- **Gemini**: Utilized for enhancing the chatbot's natural language processing capabilities.
- **Streamlit**: Framework used for building the web interface, allowing for an interactive and seamless user experience.

## Features

- **Interactive Chat Interface**: Users can engage with the chatbot to get answers to their admission-related questions.
- **Nonsense Input Checking**: The chatbot intelligently handles irrelevant inputs to improve user interaction.
- **API Integration**: The application connects to external APIs to provide up-to-date information.

## Getting Started

### How to Create Environment:

1. **Create a Virtual Environment**:
   ```bash
   python -m venv nameofENV
   ```
   Example:
   ```bash
   python -m venv AdBot
   ```

2. **Activate the Virtual Environment**:
   - **Windows**:
     ```bash
     AdBot\Scripts\activate
     ```
   - **Linux/Mac**:
     ```bash
     source AdBot/bin/activate
     ```

   **If using Conda**:
   - Create a Conda environment:
     ```bash
     conda create --name myenv
     ```
   - Specify Python version: 
     ```bash
     conda create --name myenv python=3.9
     ```

   - **Activate Conda Environment**:
     ```bash
     conda activate myenv
     ```

### Needed to Do in the Terminal

Install the required packages:
```bash
pip install google-generativeai streamlit python-dotenv langdetect nltk
```

### Version Needed

Make sure you have Python version 3.9 or higher:
```bash
python --version
```
Example output: `Python 3.12`

### Environment Variables

Since our GitHub repository is public:
- Create a `.env` file.
- Add your API key:
  ```
  API_KEY = "your-api-key"
  ```

### Contributors
