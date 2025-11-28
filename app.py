print("--- Starting RAGTube Server... ---")
from flask import Flask,render_template,request,jsonify
from backend.simple_downloader import download_transcript
from backend.rag_logic import create_vector_db,retrieve_context,generate_answer
import datetime
import os
app=Flask(__name__)

#-------------------------------------------#/Home route--------------------------------------------------------------------
@app.route("/")#--->Home page
def home():
    return render_template("index.html")


#-------------------------------------------#-/Ingestion route--------------------------------------------------------
@app.route("/ingest",methods=["POST"])#--->when user submits a YouTube URL
def ingest_video():
    data=request.json ##reads the JSON body sent from the frontend.
    video_url=data.get("url")##extract the URL from JSON.

    if not video_url:
        return jsonify({"Error","No URL provided "}),400
    print(f"Server: Received  URL{video_url}")

    #1-->Download Transcript
    success=download_transcript(video_url)
    if not success:
        return jsonify({"Error!","Failed to downlaod the transcript "}),500
    #Now we will move the file to root if its not there 

    if os.path.exists("backend/transcript_data.en.vtt"):
        os.rename("backend/transcript_data.en.vtt","transcript_data.en.vtt")

    # 2--> Create Knowledge Base
    # Now We will pass the URL just for metadata; the logic reads the .vtt file
    try:
        create_vector_db([video_url])
        return jsonify({"message":"Video processed successfully!!..Ready to chat"})
    except Exception as e:
        return jsonify({"error":str(e)}),500
    
    #----------------------------------------------------------#/chat route-----------------------------------------
@app.route("/chat",methods=["POST"])#-->This is our RAG query step.-->when user asks a question
def chat():
    try:
        data = request.json
        user_query = data.get('query')
        
        # 1. Retrieve Raw Chunks
        results = retrieve_context(user_query)
        
        if not results:
            return jsonify({"answer": "No relevant info found.", "sources": []})

        # 2. Generate LLM Answer
        ai_response = generate_answer(user_query, results)
        
        # 3. Format Sources (with HH:MM:SS)
        sources = []
        for doc in results:
            video_id = "unknown"
            seconds = 0
            
            if hasattr(doc, 'metadata') and doc.metadata:
                source = doc.metadata.get('source', '')
                if "v=" in source:
                    video_id = source.split("v=")[-1].split("&")[0]
                elif "youtu.be" in source:
                    video_id = source.split("/")[-1].split("?")[0]
                    
                seconds = int(doc.metadata.get('start_time', 0))

            # Helper to convert seconds to HH:MM:SS
            time_str = str(datetime.timedelta(seconds=seconds))
            # we can Remove "0:" if it's less than an hour for cleaner look 
            if time_str.startswith(":"):
                time_str = time_str[2:] 

            link = f"https://youtu.be/{video_id}?t={seconds}"

            sources.append({
                "time_display": time_str, # e.g. "05:30"
                "link": link,
                "snippet": doc.page_content[:100] + "..." # Just a preview
            })

        # Return the AI Answer AND the Sources
        return jsonify({
            "answer": ai_response,
            "sources": sources
        })

    except Exception as e:
        print(f"SERVER ERROR: {e}")
        return jsonify({"error": str(e)}), 500
if __name__ == '__main__':
    print("--- Web Server Starting Now! ---") # <--- Add this at the bottom
    app.run(debug=True)
