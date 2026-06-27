from langchain_openai import OpenAIEmbeddings

def get_embedding():
    """
    Get the OpenAI embeddings model
    """
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    return embeddings