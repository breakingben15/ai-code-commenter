import google.generativeai as genai
import os

# --- Configuration ---
# IMPORTANT: Replace "YOUR_API_KEY" with your actual API key.
# Make sure to keep this key private and secure.
genai.configure(api_key="AIzaSyAjmnjNl-Y42JDxfQdHAhi11ZRAiQosiBw")
model = genai.GenerativeModel('gemini-1.5-flash')

# --- Main Script Logic ---

# 1. Get the input filename from the user.
input_filename = input("Enter the name of the Python file you want to comment: ")

# 2. Check if the file exists and handle errors.
try:
    print(f"Reading {input_filename}...")
    with open(input_filename, 'r') as file:
        all_code = file.read()

    # 3. Create a unique output filename to avoid overwriting.
    base_name = f"commented_{input_filename.replace('.py', '')}"
    extension = ".py"
    output_filename = base_name + extension
    count = 1
    while os.path.exists(output_filename):
        output_filename = f"{base_name}({count}){extension}"
        count += 1

    # 4. Build a detailed prompt for the AI.
    prompt = f"""
    Your task is to act as an expert Python programmer documenting a script.
    Add a concise, one-line comment directly above each functional line of the following Python code.
    Do not add comments to blank lines, lines that are already comments, or import statements.
    Do not change the original code.
    Return only the fully commented Python code.

    Here is the script:
    {all_code}
    """

    # 5. Call the AI and get the commented code.
    print("Generating comments with AI... this may take a moment.")
    response = model.generate_content(prompt)
    commented_code = response.text

    # 6. Write the result to the new, unique file.
    print(f"Writing to {output_filename}...")
    with open(output_filename, 'w') as file:
        file.write(commented_code)
    
    print(f"Done! Your new file '{output_filename}' is ready.")

# Handle the case where the file doesn't exist.
except FileNotFoundError:
    print(f"Error: The file '{input_filename}' was not found. Please check the name and try again.")
# Handle any other potential errors during the API call.
except Exception as e:
    print(f"An unexpected error occurred: {e}")