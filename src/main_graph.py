
from state.state import CTIState
from langgraph.graph import StateGraph, START, END
from node_1_crawl_and_split.Node1 import Node1
from node_2_filter_agent.node2 import Node2
from node_3_extract_IOC.node3 import Node3
from node_4_extract_CE.node4 import Node4
from node_5_mapping.node5 import Node5
from node_6_identification_agent.node6 import Node6
# State Graph Builder
builder = StateGraph(CTIState)

# Build Nodes
builder.add_node("Node_1_crawl_and_split", Node1)
builder.add_node("Node_2_filter_agent", Node2)
builder.add_node("Node_3_extract_IOC", Node3)
builder.add_node("Node_4_extract_CE", Node4)
builder.add_node("Node_5_mapping", Node5)
builder.add_node("Node_6_identification", Node6)
# Build Edges
builder.add_edge(START, "Node_1_crawl_and_split")
builder.add_edge("Node_1_crawl_and_split", "Node_2_filter_agent")
builder.add_edge("Node_2_filter_agent", "Node_3_extract_IOC")
builder.add_edge("Node_3_extract_IOC", "Node_4_extract_CE")
builder.add_edge("Node_4_extract_CE", "Node_5_mapping")
builder.add_edge("Node_5_mapping", "Node_6_identification")
builder.add_edge("Node_6_identification", END)

# Conditional edges from CheckerAgent
# builder.add_conditional_edges(
#     "CheckerAgent",
#     should_continue,
#     {
#         "execute_builder": "Execute_Builder",
#         "end": END
#     }
# )



# Compile graph
graph = builder.compile()