from typing import Any, Dict, List, Sequence
import os


def estimate_tokens(text: str) -> int:
    """Estimate token count using `tiktoken` when available, otherwise fallback.

    Uses `encoding_for_model` when possible. Falls back to simple word-based
    heuristic if `tiktoken` is not installed.
    """
    if not text:
        return 0
    try:
        import tiktoken

        model = os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo")
        try:
            enc = tiktoken.encoding_for_model(model)
        except Exception:
            # fallback to common encoding
            enc = tiktoken.get_encoding("cl100k_base")
        return len(enc.encode(text))
    except Exception:
        words = len(text.split())
        return int(words * 1.3)


def combined_documents_text(docs: Sequence[Any]) -> str:
    """Return a single text representing the list of docs.

    Accepts either plain strings or objects with `page_content`.
    """
    parts: List[str] = []
    for d in docs:
        if d is None:
            continue
        if isinstance(d, str):
            parts.append(d)
        else:
            # langchain Document-like objects typically have `page_content`
            parts.append(getattr(d, "page_content", str(d)))
    return "\n\n".join(parts)


def prune_documents_by_token_budget(docs: Sequence[Any], max_tokens: int) -> List[Any]:
    """Keep documents until the token budget is exhausted (simple left-to-right).

    This is a simple, deterministic pruning strategy. You can replace with
    smarter ranking or summarization later.
    """
    kept = []
    tokens_used = 0
    for d in docs:
        text = d if isinstance(d, str) else getattr(d, "page_content", str(d))
        t = estimate_tokens(text)
        if tokens_used + t > max_tokens:
            break
        kept.append(d)
        tokens_used += t
    return kept


def summarize_documents(docs: Sequence[Any], max_chars_per_doc: int = 800) -> List[str]:
    """Lightweight summarization fallback: truncate each document.

    Prefer calling a real summarization chain (in `graph.chains`) from nodes.
    """
    summaries: List[str] = []
    for d in docs:
        text = d if isinstance(d, str) else getattr(d, "page_content", str(d))
        summary = text[:max_chars_per_doc]
        summaries.append(summary)
    return summaries


def store_tool_result(state: Dict[str, Any], key: str, result: Any) -> None:
    """Store `result` under `state['tool_results'][key]`, creating structure if missing."""
    if "tool_results" not in state or state["tool_results"] is None:
        state["tool_results"] = {}
    state["tool_results"][key] = result


def should_inject_full_context(docs: Sequence[Any], max_tokens: int) -> bool:
    """Return True if combined docs fit in `max_tokens` (approx).

    This lets nodes decide whether to inject full context into the prompt or
    fall back to summaries/tool-result pointers.
    """
    combined = combined_documents_text(docs)
    return estimate_tokens(combined) <= max_tokens


def get_token_budget_from_env(default: int = 3000) -> int:
    try:
        return int(os.environ.get("RAG_TOKEN_BUDGET", default))
    except Exception:
        return default
