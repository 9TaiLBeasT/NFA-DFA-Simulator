import networkx as nx
import matplotlib.pyplot as plt

def draw_automaton(states, transitions, start_state=None, final_states=None, highlight_state=None, previous_states=None):
    G = nx.DiGraph()

    # Add nodes
    for state in states:
        G.add_node(state)

    # Organizing transitions properly
    combined_transitions = {}
    for (src, symbol), destinations in transitions.items():
        for dest in destinations:
            key = (src, dest)
            if key not in combined_transitions:
                combined_transitions[key] = set()  # Use set to avoid duplicates
            combined_transitions[key].add(symbol)

    # Add edges with labels
    for (src, dest), symbols in combined_transitions.items():
        label = ','.join(sorted(symbols))  # Sort for better readability
        G.add_edge(src, dest, label=label)

    # Node colors
    node_colors = []
    for state in G.nodes:
        if state == highlight_state:
            node_colors.append("#FFD700")  # Bright yellow for current state
        elif previous_states and state in previous_states:
            node_colors.append("#90EE90")  # Light green for previous states
        elif final_states and state in final_states:
            node_colors.append("#FF6B6B")  # Red for final states
        elif state == start_state:
            node_colors.append("#4CAF50")  # Green for start state
        else:
            node_colors.append("#87CEEB")  # Sky blue for regular states

    # Positioning
    pos = nx.spring_layout(G, seed=42)  # Consistent layout

    # Draw base graph
    fig, ax = plt.subplots(figsize=(8, 5))
    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=1500, edge_color="black", font_size=10, ax=ax)

    # Add edge labels
    edge_labels = {(src, dest): data["label"] for src, dest, data in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)

    # Explicitly handle self-loops
 
    # Adjust self-loop labels separately
    for src, dest in G.edges():
        if src == dest:  # Self-loop
            pos_offset = (pos[src][0] + 0.05, pos[src][1] + 0.05)  # Adjust position slightly
            edge_labels[(src, dest)] = "\n".join(sorted(combined_transitions[(src, dest)]))  # Ensure correct format

    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)

    return fig
