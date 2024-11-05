from flask import Flask, request, jsonify
from flask_cors import CORS
from src.doc_processing import DocumentProcessor
from src.embeddings import EmbeddingIndexer
from src.rag import RAGChain

app = Flask(__name__)
CORS(app)

processor = DocumentProcessor("data/soccer_tactics")
documents = processor.load_and_split_documents()
indexer = EmbeddingIndexer()
vectorstore = indexer.create_vectorstore(documents)
chatbot = RAGChain(vectorstore).create_chain()

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    response = chatbot({"question": data['message']})
    return jsonify({"answer": response["answer"]})

if __name__ == '__main__':
    app.run(debug=True, port=5000)