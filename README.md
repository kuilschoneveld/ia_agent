# IA Agent Project

## Setup

1. Clone this repository
2. Create a `.env` file in the project root using `.env.example` as a template
3. Add your Twitter API credentials to the `.env` file

## Environment Variables

This project uses environment variables to store sensitive information like API keys. To set up:

1. Copy `.env.example` to a new file named `.env` (which is ignored by git)
2. Replace the placeholder values with your actual Twitter API credentials

Example:
```
TWITTER_CONSUMER_KEY=your_actual_key_here
TWITTER_CONSUMER_SECRET=your_actual_secret_here
...
```

## Running the Project

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Make sure NLTK data is downloaded:
   ```
   python -c "import nltk; nltk.download('punkt')"
   ```

3. Navigate to the project directory:
   ```
   cd "Ontology and SPARQL/Project"
   ```

4. Run the main script:
   ```
   python main.py
   ```

5. Enter a statement or scenario when prompted. The agent will analyze it and tell you whether it thinks the information is true or false.

6. Type "Bye" to exit the program. 