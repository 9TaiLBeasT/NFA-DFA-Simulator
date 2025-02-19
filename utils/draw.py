# draw.py
import networkx as nx
import matplotlib.pyplot as plt

def draw_automaton(states, transitions, start_state=None, final_states=None, 
                  highlight_state=None, previous_states=None):
    """Creates a visualization of the automaton using NetworkX and Matplotlib."""
    
    G = nx.MultiDiGraph()  # Changed to MultiDiGraph to better handle multiple edges
    
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
    
    # Create layout with more space
    pos = nx.spring_layout(G, k=2.0, seed=42)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Draw nodes first
    nx.draw_networkx_nodes(G, pos,
                          node_color=['#FFD700' if state == highlight_state
                                    else '#90EE90' if previous_states and state in previous_states
                                    else '#FF6B6B' if final_states and state in final_states
                                    else '#4CAF50' if state == start_state
                                    else '#87CEEB' for state in G.nodes],
                          node_size=1500)
    
    # Draw node labels
    nx.draw_networkx_labels(G, pos, font_size=10)
    
    # Handle edges and labels
    edge_labels = {}
    
    for (src, dest), symbols in combined_transitions.items():
        label = ','.join(sorted(symbols))
        if src == dest:
            # Self-loop
            G.add_edge(src, dest, label=label)
            # Draw self-loop with large arc
            nx.draw_networkx_edges(G, pos,
                                 edgelist=[(src, dest)],
                                 connectionstyle=f'arc3, rad=0.5',
                                 arrowsize=20)
            # Position label above the loop
            edge_labels[(src, dest)] = label
        else:
            # Regular transition
            G.add_edge(src, dest, label=label)
            nx.draw_networkx_edges(G, pos,
                                 edgelist=[(src, dest)],
                                 arrowsize=20)
            edge_labels[(src, dest)] = label
    
    # Draw edge labels with offset for better visibility
    pos_attrs = {}
    for (src, dest), label in edge_labels.items():
        if src == dest:
            # Position self-loop labels above the loop
            pos_attrs[(src, dest)] = {'pos': (0.3, 0.3)}
    
    nx.draw_networkx_edge_labels(G, pos,
                                edge_labels=edge_labels,
                                bbox=dict(facecolor='white', edgecolor='none', alpha=0.7),
                                font_size=9)
    
    plt.axis('off')
    return fig
