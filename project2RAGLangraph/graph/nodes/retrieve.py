from typing import Any,Dict

from graph.state import GraphState
from ingestion import retriever

def retrieve(state:GraphState)-> Dict[str,Any]:
    """
    Retrieve relevant documents based on the question in the state.

    Args:
        state: GraphState containing the question

    Returns:
        A dictionary with retrieved documents
    """
    print("Retrieving relevant documents for the question.")
    question = state["question"]
    retrieved_docs = retriever.invoke(question)
    return {"documents": retrieved_docs,"question": question}