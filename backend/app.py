# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from src.doc_processing import DocumentProcessor
from src.embeddings import EmbeddingIndexer
from src.rag import RAGChain
import os
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)

load_dotenv()

try:
    # Initialize chatbot
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

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        if not data or 'message' not in data:
            return jsonify({"error": "No message provided"}), 400
        
        response = chatbot({"question": data['message']})
        return jsonify({"answer": response["answer"]})
    
    except Exception as e:
        print(f"Error processing chat: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)