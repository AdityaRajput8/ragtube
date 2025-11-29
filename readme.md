# 🎥 RAGTube: AI Video Assistant

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.0%2B-green?style=for-the-badge&logo=flask&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-RAG-orange?style=for-the-badge&logo=chainlink&logoColor=white)
![Gemini](https://img.shields.io/badge/Google%20Gemini-AI-magenta?style=for-the-badge&logo=google&logoColor=white)

**RAGTube** is an AI-powered tool that allows you to "chat" with YouTube videos. It processes video transcripts using **Retrieval-Augmented Generation (RAG)** and **Google Gemini** to answer your questions with precise context from the video.

---

## 📋 Prerequisites

Before you begin, ensure you have the following installed on your machine:
* [Python 3.10 or higher](https://www.python.org/downloads/)
* [Git](https://git-scm.com/downloads)
* A **Google Cloud API Key** (for Gemini) - [Get it here](https://aistudio.google.com/)

---

## ⚙️ Installation & Setup Guide

Follow these steps exactly to get the project running on your local machine.

### Step 1: Clone the Repository
Open your terminal (Command Prompt, PowerShell, or Terminal) and run:

```bash
git clone [https://github.com/YOUR_GITHUB_USERNAME/RAGTube-AI-assistant.git](https://github.com/YOUR_GITHUB_USERNAME/RAGTube-AI-assistant.git)

##📂 Project Structure

Here is an overview of the codebase to help you navigate:

```bash
RAGTube(AI-assistant)/
├── backend/
│   ├── rag_logic.py         # Core RAG pipeline (Loading, Embedding, QA Chain)
│   └── simple_downloader.py # Utility to handle video transcripts
├── faiss_index/             # Stores the generated vector database locally
├── templates/
│   └── index.html           # Simple frontend interface
├── app.py                   # Main Flask application entry point
├── transcript_data.en.vtt   # The raw transcript file (Input data)
├── requirements.txt         # Project dependencies
└── .env                     # API Keys (Not included in repo)