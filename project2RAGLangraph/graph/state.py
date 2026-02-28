from typing import Any, Dict, List, TypedDict


class GraphState(TypedDict):
    """
    represents the state of our graph

    Attributes:
        question: question
        generation: LLM generation
        web_search: whether to add web search
        documents: list of documents
        tool_results: optional store for tool outputs (separated from prompt context)
        recursion_depth: depth counter to avoid infinite corrective loops
        token_budget: maximum allowed tokens for prompt context (approx)
    """
    question: str
    generation: str
    web_search: bool
    documents: List[Any]
    tool_results: Dict[str, Any]
    recursion_depth: int
    token_budget: int