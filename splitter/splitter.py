from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_documents(document):
    """
    Split the document into chunks for embedding
    """
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    split_docs = splitter.split_documents(document)
    return split_docs