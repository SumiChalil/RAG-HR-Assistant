import os
from dotenv import load_dotenv
from loader.pdf_loader import load_pdf
from splitter.splitter import split_documents
from embedding.openai_embeddings import get_embedding
from vectorstore.chroma_store import create_chroma_store, load_chroma_store
from retriever.retriever import get_retriever
from chain.rag_chain import build_rag_chain

load_dotenv()

PDF_PATH = "data/employee_handbook.pdf"
PERSIST_DIR ="hr_db"

class RAGService:
    def __init__(self):
        embeddings = get_embedding()

        if not os.path.exists(PERSIST_DIR):
            print("Creating the New HR DB...")
            document = load_pdf(PDF_PATH)
            chunks = split_documents(document)
            vectorstore = create_chroma_store(chunks, embeddings, persist_dir=PERSIST_DIR)
        else:
            print("Loading the existing HR DB...")
            vectorstore = load_chroma_store(embeddings, persist_dir=PERSIST_DIR)
        self.retriever = get_retriever(vectorstore)
        self.rag_chain = build_rag_chain(self.retriever)
    
    def ask(self, query: str) -> str:
        """
        Ask a question to the RAG chain and get the answer
        """
        return self.rag_chain.invoke(query)

def main():
    rag = RAGService()

    print("Employee Handbook RAG Application")
    print("Type 'exit' to quit.")

    while True:
        query = input("\nEnter your question: ")
        if query.lower() == "exit":
            print("Exiting the Application. Goodbye !")
            break
        answer = rag.ask(query)
        print(f"Answer: {answer}")

if __name__ == "__main__":
    main()

