from typing import Any, Dict, List
from graph.chains.generation_chain import build_generation_chain
from graph.chains.summarization_chain import build_summarization_chain
from graph.state import GraphState
from graph import utils
import os

generation_chain = build_generation_chain()


def generate(state: GraphState) -> Dict[str, Any]:
        """Generate final answer while protecting against token explosion.

        Strategies applied here:
        - Use a token budget (from `RAG_TOKEN_BUDGET`) to decide whether to inject
            full document context into the prompt.
        - If too large, store full documents in `state['tool_results']['documents']`
            and pass lightweight summaries to the LLM prompt instead.
        - Log token estimates so the flow can be monitored.
        """
        print("---GENERATE ----")
        question = state["question"]
        documents: List[Any] = state.get("documents", [])

        token_budget = state.get("token_budget") or utils.get_token_budget_from_env()

        # Decide whether to inject full context
        can_inject = utils.should_inject_full_context(documents, token_budget)
        combined_text = utils.combined_documents_text(documents)
        est_tokens = utils.estimate_tokens(combined_text)
        print(f"[monitor] estimated tokens for context: {est_tokens}; budget: {token_budget}")

        if can_inject:
                context_for_prompt = documents
                print("[monitor] injecting full context into generation prompt")
        else:
                # prune documents deterministically to fit budget
                pruned = utils.prune_documents_by_token_budget(documents, token_budget)

                # Attempt to summarize using a summarization chain; fall back to simple truncation
                try:
                        summarizer = build_summarization_chain()
                        summaries = [
                                summarizer.invoke({"text": utils.combined_documents_text([d])})
                                for d in pruned
                        ]
                except Exception:
                        summaries = utils.summarize_documents(pruned, max_chars_per_doc=800)

                # store the full documents separately in tool_results so tools/UIs can fetch them
                utils.store_tool_result(state, "documents", documents)
                utils.store_tool_result(state, "pruned_documents", pruned)
                utils.store_tool_result(state, "document_summaries", summaries)
                context_for_prompt = "\n\n".join(summaries)
                print("[monitor] context too large — stored full docs in state['tool_results'] and passing summaries")

        generation = generation_chain.invoke({"question": question, "context": context_for_prompt})

        # Save generation and maintain documents/tool-results in state
        state["generation"] = generation
        return {"generation": generation, "question": question, "documents": documents}