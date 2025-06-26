import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from typing import Optional, TypedDict, List, Dict
from agents.connector import connector_agent
from agents.parser import parser_agent

load_dotenv()

## define state class
class RepoState(TypedDict, total=False):
    repo_url: str
    local_repo_path: Optional[str]
    clone_status: Optional[str]
    error: Optional[str]
    parsed_files: List[Dict]

## create LangGraph
def build_graph():
    builder = StateGraph(RepoState)
    builder.add_node("ConnectorAgent", connector_agent)
    builder.add_node("ParserAgent", parser_agent)

    builder.set_entry_point("ConnectorAgent")
    builder.add_edge("ConnectorAgent", "ParserAgent")
    builder.set_finish_point("ParserAgent")
    return builder.compile()

if __name__ == "__main__":
    graph = build_graph()

    initial_state = RepoState({
        "repo_url" : "https://github.com/diwakar-tiwari/Ollama_Langchain"
    })
    final_state = graph.invoke(initial_state)
    print("Final State:", final_state)

    print("Final parsing summary:\n")
    for file in final_state.get("parsed_files",[]):
        print(f"File: {file['file_path']}")
        print(f"Language: {file['language']}")
        print(f"Lines: {file['lines']}")
        print(f"Functions: {file['functions']}")
        print(f"Classes: {file['classes']}")