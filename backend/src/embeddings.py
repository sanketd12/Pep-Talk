# embeddings_indexer.py
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

class EmbeddingIndexer:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings()
        
    def create_vectorstore(self, documents):
        batch_size = 5000
        vectorstore = None
        

        for i in range(0, len(documents), batch_size):
            batch = documents[i:i + batch_size]
            
            if vectorstore is None:

                vectorstore = Chroma.from_documents(
                    documents=batch,
                    embedding=self.embeddings,
                    persist_directory="soccer_coach_db"
                )
            else:

                vectorstore.add_documents(documents=batch)

            vectorstore.persist()
            
        return vectorstore