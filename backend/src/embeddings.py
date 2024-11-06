from langchain.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
import chromadb
from chromadb.config import Settings

class EmbeddingIndexer:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings()
        self.client = chromadb.PersistentClient(
            path="soccer_coach_db",
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True,
                is_persistent=True
            )
        )
        self.batch_size = 5000  # Safe batch size below ChromaDB's limit
    
    def create_vectorstore(self, documents):
        try:
            vectorstore = None
            
            # Process documents in batches
            for i in range(0, len(documents), self.batch_size):
                batch = documents[i:i + self.batch_size]
                print(f"Processing batch {i//self.batch_size + 1} of {len(documents)//self.batch_size + 1}")
                
                if vectorstore is None:
                    # Create initial vectorstore with first batch
                    vectorstore = Chroma.from_documents(
                        documents=batch,
                        embedding=self.embeddings,
                        persist_directory="soccer_coach_db",
                        client=self.client,
                        collection_name="soccer_tactics"
                    )
                else:
                    # Add subsequent batches
                    vectorstore.add_documents(documents=batch)
                
                # Persist after each batch
                vectorstore.persist()
                print(f"Processed and persisted {min(i + self.batch_size, len(documents))} documents")
            
            return vectorstore
            
        except Exception as e:
            print(f"Error creating vectorstore: {str(e)}")
            raise