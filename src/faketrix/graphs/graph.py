from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from faketrix.graphs.nodes import GraphNodes
from faketrix.graphs.state import FakeEmailState


class ConfigSchema(TypedDict):
    sender: str


graph_nodes = GraphNodes()
graph = StateGraph(FakeEmailState, config_schema=ConfigSchema)

graph.add_node("generate_declaration", graph_nodes.generate_declaration)
graph.add_node("generate_order", graph_nodes.generate_order)
graph.add_node("generate_question", graph_nodes.generate_question)
graph.add_node("generate_complaint", graph_nodes.generate_complaint)
graph.add_node("body_to_html", graph_nodes.body_to_html)
graph.add_node("send_email", graph_nodes.send_email)

graph.add_conditional_edges(
    START,
    graph_nodes.email_types,
    {
        "order": "generate_order",
        "generate_declaration": "generate_declaration",
        "question": "generate_question",
        "complaint": "generate_complaint",
    },
)

graph.add_edge("generate_order", "body_to_html")
graph.add_edge("generate_declaration", "body_to_html")
graph.add_edge("generate_question", "body_to_html")
graph.add_edge("generate_complaint", "body_to_html")
graph.add_edge("body_to_html", "send_email")
graph.add_edge("send_email", END)


graph = graph.compile()


__all__ = ["graph"]
