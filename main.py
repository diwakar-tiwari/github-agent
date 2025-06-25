import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from typing import Optional, TypedDict
from agents.connector import connector_agent

load_dotenv()

def test_agent(state):
    print("Hello from test agent, received state: ", state)
    return state # pass the same state forward

## define state class
class RepoState(TypedDict,):
    repo_url: str
    local_repo_path: Optional[str]
    clone_status: Optional[str]
    error: Optional[str]

## create LangGraph
def build_graph():
    builder = StateGraph(RepoState)
    builder.add_node("ConnectorAgent", connector_agent)
    builder.set_entry_point("ConnectorAgent")
    builder.set_finish_point("ConnectorAgent")
    return builder.compile()

if __name__ == "__main__":
    graph = build_graph()

    initial_state = RepoState({
        "repo_url" : "https://github.com/diwakar-tiwari/Ollama_Langchain"
    })
    final_state = graph.invoke(initial_state)
    print("Final State:", final_state)