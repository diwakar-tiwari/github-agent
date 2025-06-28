import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from typing import Optional, TypedDict, List, Dict
from agents.connector import connector_agent
from agents.parser import parser_agent
from agents.commentor import commentor_agent

load_dotenv()

## define state class
class RepoState(TypedDict, total=False):
    repo_url: str
    local_repo_path: Optional[str]
    clone_status: Optional[str]
    error: Optional[str]
    parsed_files: List[Dict]
    comments_summary: List[Dict]

## create LangGraph
def build_graph():
    builder = StateGraph(RepoState)
    builder.add_node("ConnectorAgent", connector_agent)
    builder.add_node("ParserAgent", parser_agent)
    builder.add_node("CommentorAgent", commentor_agent)

    builder.set_entry_point("ConnectorAgent")
    builder.add_edge("ConnectorAgent", "ParserAgent")
    builder.add_edge("ParserAgent", "CommentorAgent")
    builder.set_finish_point("CommentorAgent")
    return builder.compile()

if __name__ == "__main__":
    graph = build_graph()

    initial_state = RepoState({
        "repo_url" : "https://github.com/diwakar-tiwari/Ollama_Langchain"
    })
    final_state = graph.invoke(initial_state)
    print("Final State:", final_state)

    print("Comments extracted from repo:")
    for file_comments in final_state.get("comments_summary", []):
        print(f"File: {file_comments['file_path']}")
        print(f"Language: {file_comments['language']}")
        print(f"Single line comments: {len(file_comments['single_line_comments'])}")
        print(f"Docstrings / Multi-line comments: {len(file_comments['docstrings'])}")
