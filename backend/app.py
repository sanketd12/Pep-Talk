# backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from src.doc_processing import DocumentProcessor
from src.embeddings import EmbeddingIndexer
from src.rag import RAGChain
import os
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:5173"],
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type"]
    }
})

# Load environment variables
load_dotenv()

# Initialize chatbot
try:
    print("Initializing document processor...")
    processor = DocumentProcessor("data/soccer_tactics")
    
    print("Loading documents...")
    documents = processor.load_and_split_documents()
    
    print("Creating vector store...")
    indexer = EmbeddingIndexer()
    vectorstore = indexer.create_vectorstore(documents)
    
    print("Initializing RAG chain...")
    chatbot = RAGChain(vectorstore).create_chain()
    
except Exception as e:
    print(f"Error during initialization: {str(e)}")
    raise

@app.route('/', methods=['GET', 'POST'])
def chat():
    if request.method == 'GET':
        return jsonify({
            "answer": "¡Hola! I am Pep Guardiola. Let's discuss football tactics and strategy. What would you like to know?"
        })
    
    try:
        data = request.json
        if not data or 'message' not in data:
            return jsonify({"error": "No message provided"}), 400
        
        response = chatbot({"question": data['message']})
        return jsonify({"answer": response["answer"]})
    
    except Exception as e:
        print(f"Error processing chat: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)