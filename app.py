import requests
from flask import Flask, request, jsonify
from llmproxy import generate

app = Flask(__name__)

@app.route('/')
def hello_world():
   return jsonify({"text":'Hi. There is nothing on this page - please return from where you came from!'})

@app.route('/query', methods=['POST'])
def main():
    data = request.get_json() 

    # Extract relevant information
    user = data.get("user_name", "Unknown")
    message = data.get("text", "")

    print(data)

    # Ignore bot messages
    if data.get("bot") or not message:
        return jsonify({"status": "ignored"})

    print(f"Message from {user} : {message}")

    # Generate a response using LLMProxy
    response = generate(
        model='anthropic.claude-3-haiku-20240307-v1:0',
        system='''
        You are a LaTeX/TeX programming assistant. 
        Respond only to LaTeX-related questions, providing answers backed by specific passages from the following documents:
            LaTeX For Authors - Current Version.pdf,
            LaTeX For Authors - Historic Version.pdf,
            LaTeX Package and Class Authors - Current Version.pdf,
            Package AMSMATH - User’s Guide for the amsmath Package (Version 2.1).pdf,
            Package BOOKTABS - Publication quality tables in LaTeX.pdf,
            Package GRAPHICS - Packages in the ‘graphics’ bundle.pdf.
        Use RAG to cite relevant excerpts from these documents whenever possible. 
        If a relevant answer is not found in the RAG sources, state clearly that the information is unavailable from the provided documents, and then provide a non-RAG response if necessary.
        Be restrictive to LaTeX content only. Keep responses focused, accurate, and concise. ''',
        query= message,
        temperature=0.3,
        lastk=0,
        rag_usage=True,
        rag_k=999,
        rag_threshold=0.5,
        session_id='hw04',
    )
    print(response)
    response_text = response['response']
    
    # Send response back
    print(response_text)

    return jsonify({"text": response_text})
    
@app.errorhandler(404)
def page_not_found(e):
    return "Not Found", 404

if __name__ == "__main__":
    app.run()