# main.py
import streamlit as st
from src.doc_processing import DocumentProcessor
from src.embeddings import EmbeddingIndexer
from src.rag import RAGChain

st.title("Have a quick Pep Chat")

@st.cache_resource
def initialize_chatbot():
    processor = DocumentProcessor("data/soccer_tactics")
    documents = processor.load_and_split_documents()
    indexer = EmbeddingIndexer()
    vectorstore = indexer.create_vectorstore(documents)
    return RAGChain(vectorstore).create_chain()

chatbot = initialize_chatbot()

if "messages" not in st.session_state:
    st.session_state.messages = []
    # Add Pep's introduction
    welcome_message = """¡Hola! I am Pep Guardiola. Let's discuss football, tactics, and the beautiful art of positional play. 
    Whether you want to learn about build-up play, pressing systems, or how to dominate possession - I'm here to share my philosophy. 
    Remember, every detail matters in football. What would you like to know?"""
    st.session_state.messages.append({"role": "assistant", "content": welcome_message})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask Pep about tactics..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = chatbot({"question": prompt})
        st.markdown(response["answer"])
        st.session_state.messages.append({"role": "assistant", "content": response["answer"]})