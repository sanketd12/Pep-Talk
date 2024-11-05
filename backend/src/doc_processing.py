import os
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

class DocumentProcessor:
    def __init__(self, directory_path):
        self.directory_path = directory_path
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
    
    def load_and_split_documents(self):
        documents = []
        for file in os.listdir(self.directory_path):
            if file.endswith('.pdf'):
                loader = PyPDFLoader(os.path.join(self.directory_path, file))
                documents.extend(loader.load())
        return self.text_splitter.split_documents(documents)