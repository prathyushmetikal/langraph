from typing import Any,Dict

from graph.state import GraphState
from ingestion import retriever
from graph import utils


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
    # initialize monitoring/tool-results and defaults
    if "tool_results" not in state or state["tool_results"] is None:
        state["tool_results"] = {}

    # store raw retrieval results separately (tool results separation)
    utils.store_tool_result(state, "raw_retrieval", retrieved_docs)

    # ensure recursion and token budget defaults
    state["recursion_depth"] = state.get("recursion_depth", 0)
    state["token_budget"] = state.get("token_budget", utils.get_token_budget_from_env())

    return {"documents": retrieved_docs, "question": question}