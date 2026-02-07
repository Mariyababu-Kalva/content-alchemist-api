# 🧪 Content Alchemist

**Content Alchemist** is an AI-powered YouTube intelligence tool. It transforms long, complex video transcripts into structured, actionable summaries using **FastAPI**, **Streamlit**, and the **Gemini 2.5 Flash** model.



---

## ✨ Features
* **Structured Summarization**: Generates a catchy title, a cohesive summary, and bulleted key takeaways.
* **Robust Transcript Extraction**: Supports standard YouTube URLs, Shorts, and mobile links.
* **Pydantic Data Validation**: Ensures every AI response follows a strict, predictable schema.
* **Modern Monorepo Architecture**: Clearly separated Backend (FastAPI) and Frontend (Streamlit).

## 🏗 Project Structure
```text
D:\FastApi\content-alchemist-api\
├── backend/             # FastAPI API (Business Logic & Gemini Integration)
├── frontend/            # Streamlit UI (User Interface & Visualization)
├── .env                 # Environment Secrets (API Keys)
└── requirements.txt     # Global dependencies

🚀 Getting Started
1. Prerequisites
-> Python 3.10+
-> A Google Gemini API Key (get one from AI Studio)

2. Setup
Clone the repository and install dependencies:

# Bash
-> git clone [https://github.com/YOUR_USERNAME/content-alchemist-api.git](https://github.com/YOUR_USERNAME/content-alchemist-api.git)
-> cd content-alchemist-api
-> pip install -r requirements.txt

3. Environment Configuration
-> Create a .env file in the root directory:
    Code snippet
    -> GOOGLE_API_KEY=your_api_key_here

4. Running the Application
You will need two terminals open:

    Terminal 1: Backend
        # Bash
        uvicorn backend.main:app --reload
    
    Terminal 2: Frontend
        # Bash
        streamlit run frontend/streamlit_app.py

🛠 Tech Stack
-> Backend: FastAPI, Pydantic, Google GenAI SDK
-> Frontend: Streamlit, Requests
-> LLM: Gemini 2.5 Flash

📜 License
This project is licensed under the MIT License - see the LICENSE file for details.
-> API Documentation: Mention that once the backend is running, the interactive API documentation is available at `http://127.0.0.1:8000/docs`.


## 🖼️ UI Preview
| Home Screen | Summary Result |
| :---: | :---: |
| ![Home](assets/home.png) | ![Result](assets/result.png) |
