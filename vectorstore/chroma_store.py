from langchain_community.vectorstores import Chroma

def create_chroma_store(chunks, embeddings, persist_dir="hr_db"):
    """
    Create a chroma vector store from the document chunks and embeddings
    """

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_dir
    )

    vectorstore.persist()
    return vectorstore

def load_chroma_store(embeddings, persist_dir="hr_db"):
    """
    Load the Chroma vector store from the specified directory
    """
    return Chroma(embedding_function=embeddings, persist_directory=persist_dir)