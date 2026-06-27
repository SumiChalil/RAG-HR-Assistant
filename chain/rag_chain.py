from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_core.output_parsers import StrOutputParser


def _build_prompt():
    """
    Build the prompt template for the RAG chain
    """

    return ChatPromptTemplate.from_template(
        """
        You are an HR Assistant. Answer the question strictly using the 
        context below. If the answer is not present, say "I don't know".
        context :{context}
        question : {question}
        """
    )
# Context is nothing but the retrieved documents from the vector store
# Question is the user query

def _build_llm():
    """
    Build the LLM for the RAG chain
    """
    return ChatOpenAI(model="gpt-3.5-turbo", temperature=0.0)

def build_rag_chain(retriever):
    """
    Build the RAG chain using ChatOpenai and the provided retriever.
    """
    llm = _build_llm()
    prompt = _build_prompt()
    chain = (
        {
            "context":retriever,
            "question":RunnablePassthrough()} | prompt | llm | StrOutputParser()
    )
    return chain
