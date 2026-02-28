import pprint
import os
from dotenv import load_dotenv

from graph.chains.retrieval_grader import GradeDocuments,retrieval_grader
from graph.chains.generation_chain import build_generation_chain
from ingestion import retriever


load_dotenv()


def test_retrieval_grader_answer_yes()-> None:
    question="agent memory"
    docs=retriever.invoke(question)
    doc_txt=docs[1].page_content
    
    res: GradeDocuments = retrieval_grader.invoke({"question": question, "document": doc_txt})
    assert res.binary_score=="yes"
    
    
def test_retrival_grader_answer_no() -> None:
    question = "agent memory"
    docs = retriever.invoke(question)
    doc_txt = docs[1].page_content

    res: GradeDocuments = retrieval_grader.invoke(
        {"question": "how to make pizaa", "document": doc_txt}
    )

    assert res.binary_score == "no"

# def test_generation_chain() -> None : 
#     question="agent memory"
#     docs=retriever.invoke(question)
#     generation=generation_chain.invoke({"question": question, "context": docs})
#     pprint(generation)
from graph.chains.generation_chain import build_generation_chain


def test_generation_chain():
    chain = build_generation_chain()

    result = chain.invoke({
        "question": "What is agent memory?",
        "context": "Agent memory stores conversation history."
    })
    #pprint(result)

    assert result is not None


