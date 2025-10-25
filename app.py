# app.py - Your Secure Flask Backend (Serves Frontend + API)
# app.py - Your Secure Flask Backend (Serves Frontend + API)

import os
import google.generativeai as genai
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

# --- Initialization ---
load_dotenv()

# Tell Flask where to find the static files (our index.html)
app = Flask(__name__, static_folder='static')

# Set up CORS. It's still good practice, especially for development.
CORS(app) 

# --- Securely Configure the AI ---
try:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("API key not found. Please set the GOOGLE_API_KEY environment variable.")
    genai.configure(api_key=api_key)
    # Use the stable 'gemini-pro' model to ensure compatibility and prevent errors.
    model = genai.GenerativeModel('gemini-2.5-flash')
except Exception as e:
    print(f"Error during initialization: {e}")
    model = None

# --- Route 1: The "Front Door" to Serve the Webpage ---
@app.route('/')
def serve_index():
    """Serves the main index.html file from the 'static' folder."""
    return send_from_directory(app.static_folder, 'index.html')

# --- Route 2: The "Back Door" API Endpoint ---
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
You are an expert Python programmer specializing in PEP 257 documentation standards.
Your **primary and mandatory task** is to add professional docstrings to the given Python code.
You must not change, fix, or refactor any of the existing code logic. Only add documentation.

**Documentation Rules:**

1.  **MANDATORY DOCSTRINGS:** For *every* function (`def`), you **must** add a PEP 257 compliant docstring immediately under the definition line, enclosed in `\"\"\"triple quotes\"\"\"`.
2.  **DOCSTRING CONTENT:** Each docstring **must** include:
    * A brief, one-sentence summary of the function's purpose.
    * `Args:` section: List each parameter (if any), its type, and a description.
    * `Returns:` section: Describe the return value (if any) and its type.
3.  **INLINE COMMENTS (MINIMAL):**
    * **DO NOT** add an inline comment (`#`) for every single line. This is bad practice.
    * Only add a brief inline comment (`#`) above a line *if* the logic is complex or non-obvious. For simple code, you might not need any.
    
Your priority is the `\"\"\"docstrings\"\"\"`. Return only the fully documented Python code.

---
Here is the code to document:
---

{user_code}
"""

    try:
        response = model.generate_content(prompt)
        commented_code = response.text
        return jsonify({"commented_code": commented_code})
    except Exception as e:
        print(f"An error occurred during AI generation: {e}")
        return jsonify({"error": f"An error occurred during AI generation: {e}"}), 500

# This part is only for running the app locally on your computer
if __name__ == '__main__':
    app.run(port=5000, debug=True)

