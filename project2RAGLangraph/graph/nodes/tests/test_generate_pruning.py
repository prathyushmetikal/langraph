import builtins
import pytest

from graph.nodes import generate as generate_mod


class DummyDoc:
    def __init__(self, content, source=None):
        self.page_content = content
        self.metadata = {"source": source}


def test_generate_stores_tool_results_and_passes_summaries(monkeypatch):
    # Create many large docs so that the token budget will be exceeded
    docs = [DummyDoc("word " * 2000, source=f"doc{i}") for i in range(3)]

    # monkeypatch the generation_chain.invoke to capture call arguments
    called = {}


    def fake_invoke(inputs):
        called["inputs"] = inputs
        return "MOCK_GENERATION"


    # replace the generation chain used in module with a fake
    monkeypatch.setattr(generate_mod, "generation_chain", type("C", (), {"invoke": staticmethod(fake_invoke)})())

    state = {
        "question": "What is agent memory?",
        "documents": docs,
        "tool_results": None,
        "recursion_depth": 0,
        "token_budget": 10,  # intentionally tiny to enforce pruning
    }

    result = generate_mod.generate(state)

    assert result["generation"] == "MOCK_GENERATION"
    # full documents should be stored under tool_results
    assert "documents" in state["tool_results"]
    assert state["tool_results"]["documents"] == docs

    # generation chain should have been invoked with a 'context' that is a string (summaries)
    assert "context" in called["inputs"]
    assert isinstance(called["inputs"]["context"], str)
