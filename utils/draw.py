import networkx as nx
import matplotlib.pyplot as plt

def draw_automaton(states, transitions, start_state=None, final_states=None, highlight_state=None):
    G = nx.DiGraph()

    # Add nodes
    for state in states:
        G.add_node(state)

    # Add edges with transition labels
    for (src, symbol), destinations in transitions.items():
        for dest in destinations:
            G.add_edge(src, dest, label=symbol)

    # Define node colors
    node_colors = []
    for state in G.nodes:
        if state == highlight_state:
            node_colors.append("yellow")  # Current active state
        elif final_states and state in final_states:
            node_colors.append("red")  # Final states in red
        elif state == start_state:
            node_colors.append("green")  # Start state in green
        else:
            node_colors.append("skyblue")  # Default color

    # Use shell layout for better structure
    pos = nx.shell_layout(G)

    # Create figure
    fig, ax = plt.subplots(figsize=(8, 5))
    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=1500, edge_color="black", font_size=10, ax=ax)

    # Add edge labels
    edge_labels = {(src, dest): data["label"] for src, dest, data in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)

    return fig
