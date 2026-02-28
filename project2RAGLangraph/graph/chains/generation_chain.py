# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import StrOutputParser
# from langchain_openai import ChatOpenAI


# llm=ChatOpenAI(temperature=0)
# # prompt=pull("rlm/rag-prompt")
# prompt = ChatPromptTemplate.from_template(
#     """Answer the question using the context.

#     Context:
#     {context}

#     Question:
#     {question}
#     """
#     )
# generation_chain=prompt | llm | StrOutputParser()

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI


def build_generation_chain():
    llm = ChatOpenAI(temperature=0)

    prompt = ChatPromptTemplate.from_template(
        """Answer the question using the context.

        Context:
        {context}

        Question:
        {question}
        """
    )

    return prompt | llm | StrOutputParser()
