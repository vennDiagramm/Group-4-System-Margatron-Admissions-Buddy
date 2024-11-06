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
     
3. **Environment Variables**
- Create a `.env` file.
- Add your API key:
  ```
  API_KEY = "your-api-key"
  ```

4. **Install the required packages:**
- **Type in the terminal after activating environment**:
```bash
pip install google-generativeai streamlit python-dotenv langdetect nltk
```
- **Version Needed**: Python 3.9 or higher
```bash
python --version
```
Example Output: `Python 3.12`


### Contributors

- **<span style="color:#FF6347">Marga Pilapil</span>** - [vennDiagramm](https://github.com/vennDiagramm)
- **<span style="color:#4682B4">Jhouvann Morden</span>** - [dlGuiri](https://github.com/Joooban)
- **<span style="color:#32CD32">Darwin Guirigay</span>** - [Joooban](https://github.com/dlGuiri)
- **<span style="color:#8A2BE2">Mel Macabenta</span>** - [Lumeru](https://github.com/MeruMeru09)
- **<span style="color:#FFD700">Gavin Rivera</span>** - [Watta2xTops](https://github.com/Watta2xTops)
