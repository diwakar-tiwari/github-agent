import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END

load_dotenv()

def test_agent(state):
    print("Hello from test agent, received state: ", state)
    return state # pass the same state forward

## define state class
class RepoState(dict):
    pass

## create LangGraph
def build_graph():
    builder = StateGraph(RepoState)
    builder.add_node("Test Agent", test_agent)
    builder.set_entry_point("Test Agent")
    builder.set_finish_point("Test Agent")
    return builder.compile()

if __name__ == "__main__":
    graph = build_graph()
    final_state = graph.invoke(RepoState())
    print("Final State:", final_state)