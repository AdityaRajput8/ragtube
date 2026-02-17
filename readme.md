# 🚀 NavGurukul Pre-work: RagTube Case Study

**Candidate:** Aditya Raj
**Role:** AI Engineer
**Submission Option:** Option 1 (Deep Dive)

> **Note:** This document contains the technical analysis required for the pre-work. For installation instructions, scroll to the "Setup Guide" section at the bottom.

---

## 📺 Video Walkthrough
[**▶️ Watch the 1-Minute Demo**](https://drive.google.com/file/d/1jaw-UZG0WLCxVLac9twWWp8NggY3uQme/view?usp=drive_link)

---

## Section 1: Context

### Description
**RagTube** is a RAG-based (Retrieval-Augmented Generation) tool that transforms passive video consumption into active learning. It indexes YouTube transcripts into a vector database, allowing students to "chat" with the video. It acts as a real-time AI tutor, answering questions strictly based on the lecture's context to prevent hallucinations.

### Primary Technical Constraints
1.  **Latency:** The system needed to fetch, chunk, and embed transcripts in under 5 seconds to feel "interactive."
2.  **Token Limits:** Handling 2-hour lectures required efficient semantic chunking to stay within LLM context windows without losing information.
3.  **Cost:** I optimized for a local-first architecture (FAISS + CPU) to avoid expensive managed vector cloud costs.

---

## Section 2: Technical Implementation

### Architecture Flow
`YouTube API -> Transcript -> Recursive Splitter -> Embeddings -> FAISS Index -> LLM (Gemini/OpenAI) -> User UI`

### Code Walk-Through: The Retrieval Chain
The critical logic lies in `chains.py` (or your equivalent file), where I implemented memory handling.
* **Why it matters:** Standard RAG is "stateless" (forgets the previous question). I used `ConversationalRetrievalChain` to store chat history, allowing students to ask follow-up questions like "Can you explain that last point simply?"

### Data Flow
When a user asks a question:
1.  **Embed:** The query is converted to a vector.
2.  **Search:** FAISS finds the top 5 most similar transcript chunks.
3.  **Generate:** The LLM receives a prompt: *"Answer using ONLY this context: [Chunks]"*.
4.  **Response:** The student gets a cited answer.

---

## Section 3: Technical Decisions

### 1. FAISS (Local) vs. Pinecone (Cloud)
* **Decision:** I chose **FAISS**.
* **Trade-off:** I gained speed and zero cost but lost persistence (data is lost if the server restarts). For a "study session" app, this was the right choice.

### 2. Semantic Chunking vs. Character Splitter
* **Decision:** Used `RecursiveCharacterTextSplitter`.
* **Trade-off:** It is slower to process than simple splitting, but it keeps sentences intact, ensuring the AI understands the full context of a concept.

### Scaling Bottleneck & Mitigation
* **Problem:** **"Lost in the Middle."** In very long videos, key info in the middle often gets ignored by simple vector search.
* **Mitigation:** I would implement **Re-ranking** (using a Cross-Encoder) to re-score the retrieved chunks before sending them to the LLM, ensuring higher accuracy for long-form content.

---

## Section 4: Learning
* **Mistake:** I initially fed raw transcripts directly to the LLM.
* **Lesson:** I hit token limits immediately. This forced me to learn RAG (Retrieval Augmented Generation) and vector embeddings, which is now the industry standard.

---
# 🛠️ Installation & Setup Guide
(Your existing text continues here...)
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
