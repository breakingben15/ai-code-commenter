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
@app.route('/health')
def health_check():
    return "Alive", 200

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
You are an expert Python programmer and code reviewer.
Your task is to add professional documentation and constructive suggestions to the given code.

**CRITICAL RULE: DO NOT CHANGE OR FIX ANY CODE.**
You must return the code EXACTLY as it was given.

**Documentation Rules:**

1.  **MANDATORY DOCSTRINGS:** For *every* function (`def`), you **must** add a PEP 257 compliant docstring immediately under the definition line, enclosed in `\"\"\"triple quotes\"\"\"`.
2.  **DOCSTRING CONTENT:** Each docstring **must** include:
    * A brief, one-sentence summary.
    * `Args:` section: List each parameter, its type, and a description.
    * `Returns:` section: Describe the return value and its type.
3.  **BUG IDENTIFICATION (NEW RULE):**
    * If you identify a clear bug in the code (like an infinite loop or an uninitialized variable), **DO NOT FIX IT**.
    * Instead, add a single inline comment (`#`) on the line *directly above* the bug.
    * This comment must start with `SUGGESTION:` and briefly explain the bug and the potential fix.
    * Example: `# SUGGESTION: This creates an infinite loop. Consider adding a new input() call in this else block.`
4.  **INLINE COMMENTS (MINIMAL):**
    * **DO NOT** add an inline comment for every single line.
    * Only add brief comments for complex logic *that is not* a bug.
    
Your priority is the `\"\"\"docstrings\"\"\"` and the `SUGGESTION:` comments. Return only the documented Python code.

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

@app.route('/<path:path>')
def serve_static_files(path):
    return send_from_directory(app.static_folder, path)

# This part is only for running the app locally on your computer
if __name__ == '__main__':
    app.run(port=5000, debug=True)

