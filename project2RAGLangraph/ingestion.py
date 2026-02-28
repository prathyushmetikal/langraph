from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
import os
os.environ["USER_AGENT"] = "rag-langgraph-app"

load_dotenv()

urls=[  "https://lilianweng.github.io/posts/2023-06-23-agent/",
    "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
    "https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/",
    ]

docs=[WebBaseLoader(url).load() for url in urls ]

# Each docs fetched above has a single document with the entire webpage as content. 
# We need to split it into smaller chunks for better retrieval performance.
#Each doc has a sublist of documents , we need to iterate thorugh each of them . 
#get the list of documents finallly.

doc_list=[item for sublist in docs for item in sublist]

text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=250, chunk_overlap=10 )

doc_splits = text_splitter.split_documents(doc_list)

# vectorstore = Chroma.from_documents(documents=doc_splits, embedding=OpenAIEmbeddings(), collection_name="rag-chroma",persist_directory="./.chroma") 
#vectorstore=Chroma(collection_name="rag-chroma",persist_directory="./.chroma",embedding_function=OpenAIEmbeddings())
retriever=Chroma(collection_name="rag-chroma",persist_directory="./.chroma",embedding_function=OpenAIEmbeddings()).as_retriever()



