# AI Code Commenter 🤖📝

A robust web application that uses Google's **Gemini 2.5 Flash** AI to automatically generate PEP 257 compliant docstrings and identify potential bugs in Python code.

**🔴 Live Demo:** [https://ai-code-commenter.onrender.com/](https://ai-code-commenter.onrender.com/)

## ⚡ Features
* **Automated Documentation:** Instantly adds standard docstrings to functions, including Args and Returns.
* **Smart Bug Detection:** Identifies critical issues (like `ZeroDivisionError` or infinite loops) without breaking the code.
* **Secure Backend:** Built with **Flask** and secure environment variable handling for API keys.
* **24/7 Uptime:** Integrated health checks for continuous availability.

## 🛠️ Tech Stack
* **Language:** Python 3.10+
* **Framework:** Flask
* **AI Model:** Google Gemini 2.5 Flash
* **Hosting:** Render
* **Frontend:** HTML5 / CSS3

## 🚀 How to Run Locally

1. **Clone the repository**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git)
   cd YOUR_REPO_NAME

   Install dependencies

2. **Install Dependencies**
  ```bash
  pip install -r requirements.txt
  ```
3. **Set up Environment Variables** 
  ```bash
  Create a .env file and add your Google API key:

  GOOGLE_API_KEY=your_api_key_here
  ```
4. **Run the App**
  ```bash
  python app.py
  ```
