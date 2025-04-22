# from langchain_ollama import OllamaEmbeddings, OllamaLLM;
from langchain_openai import ChatOpenAI
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage,BaseMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import tools_condition, create_react_agent
from langchain.tools import tool
from langgraph.graph.message import add_messages
from database import VectorDataBase
from tools_executor import BasicToolNode
from typing import Annotated, Union
from typing_extensions import TypedDict  

import os
from dotenv import load_dotenv

load_dotenv()

class AgentState(TypedDict):
    """State of the agent."""
    # input: str
    messages: list[BaseMessage]
    agent_outcome: Union[AgentAction, AgentFinish, None]
    intermediate_steps: Annotated[list[tuple[AgentAction, str]], add_messages]
        
api_key = os.getenv("GPT_KEY")
chromaDB = VectorDataBase()
db = chromaDB.conecta_banco_vetorial_pre_criado()
workflow = StateGraph(AgentState)
llm = ChatOpenAI(model='gpt-4o-mini', openai_api_key=api_key)

    
    
    

@tool
def salva_informacao(informacao: int) -> str:
    """
    Salva a informação no banco de dados vetorial.
    """
    res = chromaDB.write(informacao)
    print(f"Salvando informação: {informacao}")
    return res

@tool
def resgata_informacao(prompt: str) -> str:
    """
    Resgata a informação do banco de dados vetorial.
    """
    search = db.similarity_search(prompt, k=1)
    res = search[0].page_content
    print(f"Resgatando informação: {prompt}")
    return res

tools = [salva_informacao, resgata_informacao]
llm_with_tools = llm.bind_tools(tools)
agent = create_react_agent(llm_with_tools, tools)
tool_node = BasicToolNode(tools)

# def should_continue(data):
#     if isinstance(data['agent_outcome'], AgentFinish):
#         return "end"
#     else:
#         return "continue"



  
workflow.add_node("agent", agent)
workflow.add_node("tools", tool_node)
workflow.add_edge('tools', 'agent')
workflow.add_conditional_edges(
    "agent",
    tools_condition
)
workflow.set_entry_point("agent")

graph = workflow.compile()

# Vizualize the graph
try:
    img = graph.get_graph().draw_mermaid_png()
    with open("graph.png", "wb") as f:
        f.write(img)
    print('deu certo')
except Exception:
    # This requires some extra dependencies and is optional
    print(Exception)
    # print('Exception')
    pass




def stream_graph_updates(user_input: str):
    initial_state = {'messages': user_input}
    
    for event in graph.stream(initial_state):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)
            
while True:
    user_input = input("User: ")
    if user_input.lower() in ["quit", "exit", "q"]:
        print("Goodbye!")
        break
    stream_graph_updates(user_input)