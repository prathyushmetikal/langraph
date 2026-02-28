from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

import os
load_dotenv()

llm=ChatOpenAI(temperature=0)

class GradeDocuments(BaseModel):
    """Binary score for relevance check on retrieved documents. """
    
    binary_score: str= Field(description="Documents are either relevant or not relevant. Return 'yes' or 'no'")
    
structured_llm_grader=llm.with_structured_output(GradeDocuments)

system_message="""You are a grader assessing relevance of a retrieved document to a user question. \n 
    If the document contains keyword(s) or semantic meaning related to the question, grade it as relevant. \n
    Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question."""
    
grade_prompt=ChatPromptTemplate.from_messages([
    
    ("system", system_message),
    ("human", "Question: {question} \n Retrieved document \n\n : {document} \n")
])
    

retrieval_grader = grade_prompt | structured_llm_grader