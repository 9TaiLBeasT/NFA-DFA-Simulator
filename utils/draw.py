# draw.py
import networkx as nx
import matplotlib.pyplot as plt

def draw_automaton(states, transitions, start_state=None, final_states=None, 
                  highlight_state=None, previous_states=None):
    """Creates a visualization of the automaton using NetworkX and Matplotlib."""
    
    G = nx.DiGraph()
    
    # Add nodes
    for state in states:
        G.add_node(state)
    
    # Organize transitions
    combined_transitions = {}
    for (src, symbol), destinations in transitions.items():
        for dest in destinations:
            key = (src, dest)
            if key not in combined_transitions:
                combined_transitions[key] = set()
            combined_transitions[key].add(symbol)
    
    # Add edges with labels
    for (src, dest), symbols in combined_transitions.items():
        label = ','.join(sorted(symbols))
        G.add_edge(src, dest, label=label)
    
    # Node colors
    node_colors = []
    for state in G.nodes:
        if state == highlight_state:
            node_colors.append("#FFD700")  # Current state
        elif previous_states and state in previous_states:
            node_colors.append("#90EE90")  # Previous states
        elif final_states and state in final_states:
            node_colors.append("#FF6B6B")  # Final states
        elif state == start_state:
            node_colors.append("#4CAF50")  # Start state
        else:
            node_colors.append("#87CEEB")  # Regular states
    
    # Create layout
    pos = nx.spring_layout(G, seed=42)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(8, 5))
    
    # Draw base graph
    nx.draw(G, pos, with_labels=True, node_color=node_colors,
            node_size=1500, edge_color="black", font_size=10, ax=ax)
    
    # Add edge labels
    edge_labels = {(src, dest): data["label"] 
                  for src, dest, data in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)
    
    # Handle self-loops
    for src, dest in G.edges():
        if src == dest:
            pos_offset = (pos[src][0] + 0.05, pos[src][1] + 0.05)
            edge_labels[(src, dest)] = "\n".join(
                sorted(combined_transitions[(src, dest)]))
    
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)
    
    return fig
