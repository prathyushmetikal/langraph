(The file `c:\Users\prathyush.metikal\Downloads\langraph\langraph\project2RAGLangraph\README.md` exists, but is empty)
# Corrective RAG Langraph — mini README

Overview
--------
This micro-project implements a Retrieval-Augmented Generation (RAG) pipeline with a corrective step that verifies retrieved documents before generating a final answer. The pipeline is expressed as a simple state graph: retrieve → grade_documents → (websearch?) → generate.

Key concepts
------------
- Retrieval: fetch candidate chunks from a vector store (Chroma) using text embeddings.
- Grading (corrective): a structured LLM grader checks each retrieved document for relevance and sets a flag to trigger a web search when documents are irrelevant.
- Generation: a prompt + LLM chain composes the final answer from the filtered context.

Where to look
-------------
- `project2RAGLangraph/ingestion.py` — builds the `retriever` (Web loaders → text splitter → Chroma vectorstore with `OpenAIEmbeddings`).
- `project2RAGLangraph/graph/consts.py` — node name constants used by the workflow.
- `project2RAGLangraph/graph/state.py` — the `GraphState` shape (`question`, `documents`, `generation`, `web_search`).
- `project2RAGLangraph/graph/graph.py` — the graph/workflow runtime used to add nodes and edges.
- `project2RAGLangraph/graph/nodes/retrieve.py` — retrieval node that calls `ingestion.retriever`.
- `project2RAGLangraph/graph/chains/retrieval_grader.py` — structured LLM grader that returns a binary `yes`/`no` for relevance.
- `project2RAGLangraph/graph/nodes/grade_documents.py` — applies the grader and sets `web_search` when needed.
- `project2RAGLangraph/graph/chains/generation_chain.py` — prompt + LLM chain that produces final output.
- `project2RAGLangraph/graph/nodes/generate.py` — executes the generation chain.
- `project2RAGLangraph/main.py` — example orchestrator that compiles and runs the state graph.

Quick setup & run (local developer)
-----------------------------------
1. Create and activate a Python venv and install dependencies from `pyproject.toml`.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
```

2. Set environment variables (OpenAI API key required for embeddings/LLM):

```powershell
setx OPENAI_API_KEY "your_key_here"
setx USER_AGENT "rag-langgraph-app"
```

3. Run the demo script (this will build/load the Chroma store and invoke the pipeline):

```powershell
python -m project2RAGLangraph.main
```

Notes and caveats
-----------------
- The `ingestion.py` sample downloads a few web pages and builds a local Chroma vector store under `./.chroma`. The first run may be slow and requires internet and OpenAI credentials.
- The grader and generation chains use `langchain_openai`/`ChatOpenAI`. Ensure your `OPENAI_API_KEY` is set.
- Tests in `project2RAGLangraph/graph/chains/tests/test_chains.py` currently call the live retriever and chains, so running them requires the same environment and keys.

Extending the corrective flow
----------------------------
- Add a reranker node between retrieval and grading to improve top-k quality.
- Replace `WEBSEARCH` with a targeted re-retrieval that queries other sources or APIs.
- Persist document provenance (URLs/ids) into document metadata for traceability.

Contact
-------
If you want, I can (a) inspect `ingestion.py` and summarize the exact retriever stack (done), (b) run the tests here, or (c) add CI-friendly unit tests that mock external LLM/retriever calls. Tell me which next.
