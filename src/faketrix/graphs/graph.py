from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from faketrix.graphs.nodes import GraphNodes
from faketrix.graphs.state import FakeEmailState


class ConfigSchema(TypedDict):
    sender: str


graph_nodes = GraphNodes()
graph = StateGraph(FakeEmailState, config_schema=ConfigSchema)

graph.add_node("generate_fake_data", graph_nodes.generate_fake_data)
graph.add_node("generate_email", graph_nodes.generate_email)
graph.add_node("body_to_html", graph_nodes.body_to_html)
graph.add_node("send_email", graph_nodes.send_email)

graph.add_edge(START, "generate_fake_data")
graph.add_edge("generate_fake_data", "generate_email")
graph.add_edge("generate_email", "body_to_html")
graph.add_edge("body_to_html", "send_email")
graph.add_edge("send_email", END)


graph = graph.compile()


__all__ = ["graph"]
