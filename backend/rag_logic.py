import re 
import os
from langchain_community.document_loaders import YoutubeLoader
from langchain_community.document_loaders.youtube import TranscriptFormat
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.docstore.document import Document
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv 
load_dotenv()

# --- CONFIGURATION ---
MY_GOOGLE_KEY = os.getenv("GOOGLE_API_KEY")
# 1. Setting up the embedding
EMBEDDING_MODEL = GoogleGenerativeAIEmbeddings(
    model="models/text-embedding-004", 
    google_api_key=MY_GOOGLE_KEY  # Use the key variable defined above
)

# 2. Setting up the LLM
llm = ChatGoogleGenerativeAI(
    temperature=0,
    model="gemini-2.5-flash",
    google_api_key=MY_GOOGLE_KEY  # Use the key variable defined above
)

# ............................................PART-1.......................................................
def process_video(video_url):
    file_path = "transcript_data.en.vtt"
    
    if not os.path.exists(file_path):
        return []

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    documents = []
    current_chunk = ""
    current_time = 0
    
    for line in lines:
        if "-->" in line:
            time_str = line.split("-->")[0].strip()
            h, m, s = time_str.split(":")
            current_time = int(h)*3600 + int(m)*60 + float(s)
        elif line.strip() and not line.strip().isdigit():
            # NEW: Remove the weird <00:00:00> tags using Regex
            clean_line = re.sub(r'<[^>]+>', '', line)
            
            # Only add if there is text left
            if clean_line.strip():
                current_chunk += " " + clean_line.strip()
            
            if len(current_chunk) > 1000:
                doc = Document(
                    page_content=current_chunk,
                    metadata={"source": video_url, "start_time": int(current_time)}
                )
                documents.append(doc)
                current_chunk = ""

    if current_chunk:
        doc = Document(
            page_content=current_chunk,
            metadata={"source": video_url, "start_time": int(current_time)}
        )
        documents.append(doc)
    
    return documents

# ....................................................PART-2...................................................
def create_vector_db(urls):
    """
    Iterates through a list of URLs, creates vectors, and saves to disk.
    """
    all_documents = []
    
    print("--- Starting Ingestion ---")
    for url in urls:
        print(f"Processing: {url}")
        docs = process_video(url)
        all_documents.extend(docs)
        
    if not all_documents:
        print("No documents to save.")
        return

    # Create Vector Store
    print("Creating Embeddings (This may take a moment)...")
    db = FAISS.from_documents(all_documents, EMBEDDING_MODEL)
    
    # Save to a folder named 'faiss_index'
    db.save_local("faiss_index")
    print("--- Database Saved Successfully ---")

# ............................................PART-3.......................................................
def retrieve_context(query):
    """
    Loads the DB and finds relevant transcript chunks.
    """
    # Load the DB from disk
    try:
        db = FAISS.load_local("faiss_index", EMBEDDING_MODEL, allow_dangerous_deserialization=True)
        
        # Search (k=5 means get top 5 matches)
        docs = db.similarity_search(query, k=5)
        return docs
    
    except Exception as e:
        print(f"Error retrieving context: {e}")
        return []

def generate_answer(query, context_docs):
    """
    Takes the Query + retrieve chunks.-->Generates human answers..
    """
    if not context_docs:
        return "I couldnt find any relevant information in this video"
    
    # Step--1: Format the context
    context_text = "\n\n".join([doc.page_content for doc in context_docs])

    # Step--2: Creating the system prompt
    prompt_template = ChatPromptTemplate.from_template(
        """You are helpful A.I teaching asssitant!
        Answer the student's question based ONLY on the following video transcript context provided.
        Dont hallucinate. If the answer is not in the video, say "I don't know based on this video."
        
        Context:
        {context}

        Question:
        {question}
    """)
    
    # Step--3: Chain it together
    chain = prompt_template | llm
    
    # Step--4: Run the chain
    response = chain.invoke({"context": context_text, "question": query})
    return response.content