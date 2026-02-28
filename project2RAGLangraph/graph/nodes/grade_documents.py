from typing import Any, Dict

from graph.chains.retrieval_grader import retrieval_grader
from graph.state import GraphState
from graph import utils
import os


def grade_documents(state: GraphState) -> Dict[str, Any]:
    """
    Determines whether the retrieved documents are relevant to the question
    If any document is not relevant, we will set a flag to run web search

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Filtered out irrelevant documents and updated web_search state
    """

    print("---CHECK DOCUMENT RELEVANCE TO QUESTION---")
    question = state["question"]
    documents = state["documents"]

    filtered_docs = []
    web_search = False
    # ensure tool_results container exists and collect per-doc grades for monitoring
    if "tool_results" not in state or state["tool_results"] is None:
        state["tool_results"] = {}
    grades = []
    for d in documents:
        score = retrieval_grader.invoke(
            {"question": question, "document": d.page_content}
        )
        grade = score.binary_score
        grades.append({"document_id": getattr(d, "metadata", {}).get("source", None), "grade": grade})
        if grade.lower() == "yes":
            print("---GRADE: DOCUMENT RELEVANT---")
            filtered_docs.append(d)
        else:
            print("---GRADE: DOCUMENT NOT RELEVANT---")
            web_search = True
            continue
    # store grader outputs separately so they are available for audits/monitoring
    utils.store_tool_result(state, "retrieval_grades", grades)

    # handle recursion limit to avoid infinite corrective loops
    recursion_limit = int(os.environ.get("RAG_RECURSION_LIMIT", 3))
    state["recursion_depth"] = state.get("recursion_depth", 0)
    if web_search:
        state["recursion_depth"] += 1
        print(f"[monitor] web_search requested; recursion_depth={state['recursion_depth']}")
        if state["recursion_depth"] > recursion_limit:
            print(f"[monitor] recursion limit {recursion_limit} exceeded — stopping further web searches")
            web_search = False
    return {"documents": filtered_docs, "question": question, "web_search": web_search}