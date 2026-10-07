from langgraph.graph import StateGraph, START, END

from agent.state import BusinessState
from agent.nodes import business_agent


def create_business_graph():

    graph = StateGraph(BusinessState)

    graph.add_node(
        "business_agent",
        business_agent
    )

    graph.add_edge(
        START,
        "business_agent"
    )

    graph.add_edge(
        "business_agent",
        END
    )

    return graph.compile()