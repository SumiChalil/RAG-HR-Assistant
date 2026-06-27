from langchain_community.document_loaders import PyPDFLoader

def load_pdf(path: str):
    """
    Load a pdf document from the specified path
    """
    loader = PyPDFLoader(path)
    document = loader.load()
    return document
