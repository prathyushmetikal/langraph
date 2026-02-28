from typing import Any,Dict
from graph.chains.generation_chain import build_generation_chain

from graph.state import GraphState

generation_chain = build_generation_chain()
def generate(state:GraphState)-> Dict[str,Any]:
    print("---GENERATE ----")
    question = state["question"]
    documents = state["documents"]
    generation = generation_chain.invoke({"question": question, "context": documents})
    return {"generation": generation, "question": question, "documents": documents}