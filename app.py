# app.py - Your Secure Flask Backend

import os
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv # Import the new library

# --- Initialization ---
load_dotenv() # This line finds the .env file and loads the variables from it

app = Flask(__name__)
CORS(app, origins=["https://ai-code-commenter.onrender.com"])

# --- Securely Configure the AI ---
# The script now gets the key from the .env file loaded above
try:
    api_key = os.getenv("GOOGLE_API_KEY") # Use os.getenv() which reads loaded variables
    if not api_key:
        raise ValueError("API key not found. Make sure you have a .env file with GOOGLE_API_KEY='YOUR_KEY'")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    print(f"Error during initialization: {e}")
    model = None 

# --- API Endpoint ---
@app.route('/generate', methods=['POST'])
def generate():
    """Receives code from the frontend, gets comments from the AI, and returns them."""
    if not model:
        return jsonify({"error": "Server is not configured correctly. Check API key."}), 500

    data = request.get_json()
    if not data or 'code' not in data:
        return jsonify({"error": "No code provided in the request."}), 400
    
    user_code = data['code']

    prompt = f"""
    Your task is to act as an expert Python programmer documenting a script.
    Add a concise, one-line comment directly above each functional line of the following Python code.
    Do not add comments to blank lines, lines that are already comments, or import statements.
    Do not change the original code.
    Return only the fully commented Python code.

    Here is the script:
    {user_code}
    """

    try:
        response = model.generate_content(prompt)
        commented_code = response.text
        return jsonify({"commented_code": commented_code})
    except Exception as e:
        print(f"An error occurred during AI generation: {e}")
        return jsonify({"error": f"An error occurred: {e}"}), 500

# --- Run the App ---
if __name__ == '__main__':
    app.run(port=5000, debug=True)
