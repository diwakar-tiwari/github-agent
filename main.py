import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from typing import Optional, TypedDict, List, Dict
from agents.connector import connector_agent
from agents.parser import parser_agent
from agents.commentor import commentor_agent
from agents.readme_agent import readme_agent
from agents.commit_agent import commit_agent
from agents.doc_agent import doc_agent
from agents.diagram_agent import diagram_agent

load_dotenv()

## define state class
class RepoState(TypedDict, total=False):
    # Step 1: Connector Agent
    repo_url: str
    local_repo_path: str
    clone_status: str
    error: str

    # Step 2: Parser Agent
    parsed_files: List[dict]
    parsed_status: str
    parser_error: str

    # Step 3: Commentor Agent
    comments_summary: List[dict]
    commentor_status: str
    commentor_error: str

    # Step 4: Readme Agent
    readme_content: Optional[str]
    readme_status: Optional[str]

    # step 5: commit agent
    commit_history: Optional[List[dict]]
    commit_status: str

    # step 6: Docs agent
    project_docs: str

    # step 7: Diagram agent
    diagram_mermaid: Optional[str]
    diagram_status: Optional[str]


## create LangGraph
def build_graph():
    builder = StateGraph(RepoState)
    builder.add_node("ConnectorAgent", connector_agent)
    builder.add_node("ParserAgent", parser_agent)
    builder.add_node("CommentorAgent", commentor_agent)
    builder.add_node("ReadmeAgent", readme_agent)
    builder.add_node("CommitAgent", commit_agent)
    builder.add_node("DocsAgent", doc_agent)
    builder.add_node("DiagramAgent", diagram_agent)

    builder.set_entry_point("ConnectorAgent")
    builder.add_edge("ConnectorAgent", "ParserAgent")
    builder.add_edge("ParserAgent", "CommentorAgent")
    builder.add_edge("CommentorAgent", "ReadmeAgent")
    builder.add_edge("ReadmeAgent", "CommitAgent")
    builder.add_edge("CommitAgent", "DocsAgent")
    builder.set_finish_point("DocsAgent", "DiagramAgent")
    builder.add_edge("DiagramAgent", END)
    return builder.compile()

if __name__ == "__main__":
    graph = build_graph()

    initial_state = RepoState({
        "repo_url" : "https://github.com/diwakar-tiwari/Ollama_Langchain"
    })
    final_state = graph.invoke(initial_state)
    print("Final State:", final_state)

    print(final_state.get("project_docs", "No documentation generated"))


