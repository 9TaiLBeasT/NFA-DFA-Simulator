import streamlit as st

# Global state variables
states = set()
transitions = {}
start_state = None
final_states = set()

def add_state(state):
    """Adds a state to the automaton."""
    if state:
        states.add(state)

def add_transition(source, input_symbol, destination):
    """Adds a transition to the automaton."""
    if source not in states:
        st.error(f"Error: Source state '{source}' does not exist!")
        return
    if destination not in states:
        st.error(f"Error: Destination state '{destination}' does not exist!")
        return
    
    if (source, input_symbol) not in transitions:
        transitions[(source, input_symbol)] = []
    if destination not in transitions[(source, input_symbol)]:
        transitions[(source, input_symbol)].append(destination)

def set_start_state(state):
    """Sets the start state."""
    global start_state
    if state in states:
        start_state = state
    else:
        st.error(f"Error: Start state '{state}' is not in the state list!")

def add_final_state(state):
    """Adds a final state."""
    if state in states:
        final_states.add(state)
    else:
        st.error(f"Error: Final state '{state}' is not in the state list!")

def validate_automaton():
    """Checks if automaton is correctly defined."""
    if not start_state:
        st.error("Error: Start state is not set!")
        return False
    if not final_states:
        st.error("Error: No final states defined!")
        return False
    return True

def generate_from_input_string(input_string):
    """Generates an automaton from input string."""
    global start_state
    states.clear()
    transitions.clear()
    final_states.clear()
    start_state = None
    
    if not input_string:
        st.error("Error: Input string is empty!")
        return
    
    start_state = "q0"
    add_state("q0")
    current_state = "q0"
    seen_symbols = {}
    
    for i, char in enumerate(input_string):
        next_state = f"q{i + 1}"
        
        if current_state not in seen_symbols:
            seen_symbols[current_state] = set()
        
        if char not in seen_symbols[current_state]:
            add_transition(current_state, char, current_state)
            seen_symbols[current_state].add(char)
        
        if i < len(input_string) - 1:
            add_state(next_state)
            add_transition(current_state, char, next_state)
            current_state = next_state
    
    add_final_state(current_state)
    
def simulate_step_by_step(input_string):
    """Simulates the automaton step-by-step."""
    if not validate_automaton():
        return
        
    current_states = {start_state}
    
    for symbol in input_string:
        next_states = set()
        for state in current_states:
            if (state, symbol) in transitions:
                next_states.update(transitions[(state, symbol)])
                
        if not next_states:
            yield list(current_states), False
            return
            
        current_states = next_states
        yield list(current_states), None
        
    is_accepted = any(state in final_states for state in current_states)
    yield list(current_states), is_accepted

def remove_state(state):
    """Removes a state and all its related transitions."""
    global start_state
    if state in states:
        states.remove(state)
        transitions_copy = transitions.copy()
        for (src, sym) in transitions_copy.keys():
            if src == state or state in transitions_copy[(src, sym)]:
                del transitions[(src, sym)]
        if start_state == state:
            start_state = None
        if state in final_states:
            final_states.remove(state)
    else:
        st.error(f"Error: State '{state}' does not exist!")

def remove_transition(source, input_symbol):
    """Removes a specific transition."""
    if (source, input_symbol) in transitions:
        del transitions[(source, input_symbol)]
    else:
        st.error(f"Error: Transition '{source} --{input_symbol}-->' does not exist!")

def convert_to_dfa():
    """Converts NFA to DFA using subset construction."""
    new_states = set()
    new_transitions = {}
    new_start = None
    new_finals = set()
    
    initial = frozenset([start_state])
    states_to_process = [initial]
    processed_states = set()
    
    def get_state_name(state_set):
        return f"q{{{','.join(sorted(state_set))}}}"
    
    while states_to_process:
        current_states = states_to_process.pop(0)
        current_dfa_state = get_state_name(current_states)
        
        if current_states in processed_states:
            continue
            
        processed_states.add(current_states)
        new_states.add(current_dfa_state)
        
        if start_state in current_states:
            new_start = current_dfa_state
        if any(state in final_states for state in current_states):
            new_finals.add(current_dfa_state)
        
        symbols = set(symbol for state in current_states 
                     for (src, symbol) in transitions.keys() 
                     if src == state)
        
        for symbol in symbols:
            next_states = set()
            for state in current_states:
                if (state, symbol) in transitions:
                    next_states.update(transitions[(state, symbol)])
            
            if next_states:
                next_states = frozenset(next_states)
                next_dfa_state = get_state_name(next_states)
                
                if next_states not in processed_states:
                    states_to_process.append(next_states)
                
                if (current_dfa_state, symbol) not in new_transitions:
                    new_transitions[(current_dfa_state, symbol)] = []
                new_transitions[(current_dfa_state, symbol)].append(next_dfa_state)
    
    return new_states, new_transitions, new_start, new_finals

def minimize_dfa():
    """Minimizes DFA using Hopcroft's algorithm."""
    if not all(len(dests) == 1 for dests in transitions.values()):
        st.error("Cannot minimize: Input automaton must be a DFA!")
        return states, transitions, start_state, final_states

    def get_transitions_to(state, symbol):
        return {s for s in states 
               if (s, symbol) in transitions 
               and state in transitions[(s, symbol)]}

    non_final = states - final_states
    partitions = [non_final, final_states] if non_final else [final_states]
    unprocessed = [final_states]
    
    while unprocessed:
        A = unprocessed.pop(0)
        symbols = {symbol for _, symbol in transitions.keys()}
        
        for symbol in symbols:
            X = set().union(*[get_transitions_to(state, symbol) for state in A])
            
            new_partitions = []
            for Y in partitions:
                Y1 = Y & X
                Y2 = Y - X
                
                if Y1 and Y2:
                    new_partitions.extend([Y1, Y2])
                    if Y in unprocessed:
                        unprocessed.remove(Y)
                        unprocessed.extend([Y1, Y2])
                    else:
                        unprocessed.append(Y1 if len(Y1) <= len(Y2) else Y2)
                else:
                    new_partitions.append(Y)
            
            partitions = new_partitions
    
    return build_minimized_dfa(partitions)

def build_minimized_dfa(partitions):
    """Helper function to build minimized DFA from partitions."""
    new_states = set()
    new_transitions = {}
    new_start = None
    new_finals = set()
    state_mapping = {}
    
    for i, partition in enumerate(partitions):
        if not partition:
            continue
        new_state = f"q{i}"
        new_states.add(new_state)
        
        for state in partition:
            state_mapping[state] = new_state
            if state == start_state:
                new_start = new_state
            if state in final_states:
                new_finals.add(new_state)
    
    for (src, symbol), destinations in transitions.items():
        for dest in destinations:
            if src in state_mapping and dest in state_mapping:
                new_src = state_mapping[src]
                new_dest = state_mapping[dest]
                if (new_src, symbol) not in new_transitions:
                    new_transitions[(new_src, symbol)] = []
                new_transitions[(new_src, symbol)].append(new_dest)
    
    return new_states, new_transitions, new_start, new_finals

def generate_test_strings(max_length=5):
    """Generates test strings up to specified length."""
    alphabet = set(symbol for _, symbol in transitions.keys())
    if not alphabet:
        return []
    
    results = []
    
    def simulate_with_path(input_string):
        current_states = {start_state}
        path = [list(current_states)]
        
        for symbol in input_string:
            next_states = set()
            for state in current_states:
                if (state, symbol) in transitions:
                    next_states.update(transitions[(state, symbol)])
            if not next_states:
                return False, path
            current_states = next_states
            path.append(list(current_states))
        
        return any(state in final_states for state in current_states), path
    
    def generate_strings(prefix, length):
        if length > max_length:
            return
        
        if prefix:
            is_accepted, path = simulate_with_path(prefix)
            results.append((prefix, is_accepted, path))
        
        for symbol in sorted(alphabet):
            generate_strings(prefix + symbol, length + 1)
    
    generate_strings("", 0)
    return sorted(results, key=lambda x: (len(x[0]), x[0]))

def is_deterministic():
    """Checks if the automaton is deterministic."""
    return all(len(dests) == 1 for dests in transitions.values())

def simulate_with_animation(input_string):
    """Simulates with animation support."""
    if not validate_automaton():
        return []
    
    simulation_steps = []
    current_states = {start_state}
    previous_states = set()
    
    simulation_steps.append((list(current_states), "", None, previous_states))
    
    for i, symbol in enumerate(input_string):
        previous_states = current_states.copy()
        next_states = set()
        
        for state in current_states:
            if (state, symbol) in transitions:
                next_states.update(transitions[(state, symbol)])
        
        if not next_states:
            simulation_steps.append((list(current_states), symbol, False, previous_states))
            return simulation_steps
        
        current_states = next_states
        is_final = i == len(input_string) - 1
        acceptance = is_final and any(state in final_states for state in current_states)
        simulation_steps.append((list(current_states), symbol, 
                               acceptance if is_final else None, 
                               previous_states))
    
    return simulation_steps
