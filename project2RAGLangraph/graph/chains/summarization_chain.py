from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI


def build_summarization_chain():
    llm = ChatOpenAI(temperature=0)

    prompt = ChatPromptTemplate.from_template(
        """Summarize the following text into a concise paragraph (2-3 sentences):

        Text:
        {text}
        """
    )

    return prompt | llm | StrOutputParser()
