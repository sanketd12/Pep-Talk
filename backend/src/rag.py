# rag.py
import os
from dotenv import load_dotenv
from langchain_community.llms import Together
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate

class RAGChain:
    def __init__(self, vectorstore):
        load_dotenv()
        self.vectorstore = vectorstore
        
        # Create Pep Guardiola-style prompt template
        self.qa_template = """You are Pep Guardiola, the legendary football manager known for tactical innovation, positional play, and intense attention to detail. SPEAK ABOUT PEP GUARDIOLA IN FIRST PERSON
        You should respond in Pep's characteristic style, incorporating: 
        - Passionate and detailed tactical explanations
        - Emphasis on positional play (juego de posición)
        - Focus on ball possession and space creation
        - References to the importance of training and preparation
        - Occasional mentions of your experiences at Barcelona, Bayern Munich, and Manchester City
        - Use of tactical terminology like "half-spaces", "build-up play", and "pressing triggers"
        - Pep's characteristic intensity and perfectionism
        
        Context from relevant soccer documents:
        {context}
        
        Chat History:
        {chat_history}
        
        Question: {question}
        
        Pep Guardiola's Response: """
        
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            output_key="answer",
            return_messages=True
        )
        
        self.llm = Together(
            model="mistralai/Mistral-7B-Instruct-v0.2",
            temperature=0.7,
            max_tokens=512,
            together_api_key=os.getenv('TOGETHER_API_KEY')
        )
    
    def create_chain(self):
        # Create prompt from template
        qa_prompt = PromptTemplate(
            template=self.qa_template,
            input_variables=["context", "chat_history", "question"]
        )
        
        return ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vectorstore.as_retriever(search_kwargs={"k": 3}),
            memory=self.memory,
            combine_docs_chain_kwargs={"prompt": qa_prompt},
            return_source_documents=True,
            verbose=True
        )