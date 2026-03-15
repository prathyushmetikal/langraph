from typing import Annotated
from langgraph.graph import START,END,StateGraph
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import InMemorySaver

from langchain_ollama import ChatOllama
from colorama import Fore
from langgraph.prebuilt import ToolNode

from Tools.stocktool import simple_screener



#2 create llm model

llm=ChatOllama(model='qwen3:8b')

#8 Create tool 
tools=[simple_screener]

#9 Bind llm with tools

llm_with_tools=llm.bind_tools(tools)

#10 Create Tool Node

tool_node=ToolNode(tools)


#3 create a state
class State(dict):
    messages:Annotated[list,add_messages]

#4 build llm nodes

def chatbot(state):
    print(state['messages'])
    return {"messages":[llm_with_tools.invoke(state['messages'])]}

#11 Create Router Node for the conditional edge.
def router(state:State):
    last_message=state['messages'][-1]
    if hasattr(last_message,'tool_calls') and last_message.tool_calls:
        return "tools"
    else:
        return END

#5 Create our graph

graph_builder=StateGraph(State)

graph_builder.add_node("chatbot",chatbot)
graph_builder.add_node("tools",tool_node)

#12 add conditional edge and tool node 
graph_builder.add_edge(START,"chatbot")
graph_builder.add_edge("tools","chatbot")
graph_builder.add_conditional_edges("chatbot",router)

# graph_builder.add_edge("chatbot",END)

#memory capability addition
memory=InMemorySaver()
graph=graph_builder.compile(checkpointer=memory)

#7 Build the loop and run it

if __name__=='__main__':
    while True:
        prompt=input("Pass your prompt here: ")
        result=graph.invoke({"messages":[{"role":"user","content":prompt}]},config={"configurable":{"thread_id":12345}})
        print(Fore.LIGHTMAGENTA_EX + result['messages'][-1].content+Fore.RESET)