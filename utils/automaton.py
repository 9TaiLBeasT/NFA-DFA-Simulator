import streamlit as st

class Automaton:
    def __init__(self):
        self.states = set()
        self.transitions = {}
        self.start_state = None
        self.final_states = set()

    def add_state(self, state):
        """Adds a state to the automaton."""
        if state:
            self.states.add(state)


    def add_transition(self, source, input_symbol, destination):
        """Adds a transition to the automaton (works for both DFA & NFA)."""
        if source not in self.states:
            st.error(f"âŒ Error: Source state '{source}' does not exist!")
            return
        if destination not in self.states:
            st.error(f"âŒ Error: Destination state '{destination}' does not exist!")
            return
    
        # Create a unique key for each source-input_symbol pair
        if (source, input_symbol) not in self.transitions:
            self.transitions[(source, input_symbol)] = []
        
        # Add the transition if it doesn't exist
        if destination not in self.transitions[(source, input_symbol)]:
            self.transitions[(source, input_symbol)].append(destination)

    def set_start_state(self, state):
        """Sets the start state."""
        if state in self.states:
            self.start_state = state
        else:
            st.error(f"âŒ Error: Start state '{state}' is not in the state list!")

    def add_final_state(self, state):
        """Adds a final state."""
        if state in self.states:
            self.final_states.add(state)
        else:
            st.error(f"âŒ Error: Final state '{state}' is not in the state list!")

    def validate_automaton(self):
        """Checks if automaton is correctly defined."""
        if not self.start_state:
            st.error("âŒ Error: Start state is not set!")
            return False
        if not self.final_states:
            st.error("âŒ Error: No final states defined!")
            return False
        return True

    def generate_from_input_string(self, input_string):
        """
        Generates an automaton dynamically from an input string:
        - Ensures self-loops have unique symbols.
        - Prevents duplicate transitions.
        """
        self.states.clear()
        self.transitions.clear()
        self.final_states.clear()
        self.start_state = None
    
        if not input_string:
            st.error("âŒ Error: Input string is empty!")
            return
    
        self.start_state = "q0"
        self.add_state("q0")
    
        current_state = "q0"
        last_state = None
        seen_symbols = {}  # Dictionary to track self-loop symbols per state
    
        for i, char in enumerate(input_string):
            next_state = f"q{i + 1}"
    
            # Initialize symbol tracking for the current state
            if current_state not in seen_symbols:
                seen_symbols[current_state] = set()
    
            # Only add a self-loop once per unique symbol
            if char not in seen_symbols[current_state]:
                self.add_transition(current_state, char, current_state)
                seen_symbols[current_state].add(char)
    
            if i < len(input_string) - 1:
                self.add_state(next_state)
                self.add_transition(current_state, char, next_state)
                last_state = current_state
                current_state = next_state
    
        # Add the final state
        self.add_final_state(current_state)


    def simulate_step_by_step(self, input_string):
        """Simulates the automaton step-by-step."""
        if not self.validate_automaton():
            return
        current_states = {self.start_state}
        for symbol in input_string:
            next_states = set()
            for state in current_states:
                if (state, symbol) in self.transitions:
                    next_states.update(self.transitions[(state, symbol)])
            if not next_states:
                yield list(current_states), False  # No valid transitions â†’ rejection
                return
            current_states = next_states
            yield list(current_states), None  # Intermediate step
        is_accepted = any(state in self.final_states for state in current_states)
        yield list(current_states), is_accepted  # Final state check

    def remove_state(self, state):
        """Removes a state and all its related transitions."""
        if state in self.states:
            self.states.remove(state)

            # Remove transitions involving the state
            self.transitions = {
                (src, sym): dests
                for (src, sym), dests in self.transitions.items()
                if src != state and state not in dests
            }

            # Update start and final states if necessary
            if self.start_state == state:
                self.start_state = None
            if state in self.final_states:
                self.final_states.remove(state)
        else:
            st.error(f"âŒ Error: State '{state}' does not exist!")

    def remove_transition(self, source, input_symbol):
        """Removes a specific transition from the automaton."""
        if (source, input_symbol) in self.transitions:
            del self.transitions[(source, input_symbol)]
        else:
            st.error(f"âŒ Error: Transition '{source} --{input_symbol}-->' does not exist!")

    def clear_automaton(self):
        """Clears all states, transitions, and configurations."""
        self.states.clear()
        self.transitions.clear()
        self.start_state = None
        self.final_states.clear()


    #new Fetures    

    # Add these methods to your Automaton class 

    # Add these methods to your Automaton class in automaton.py

    def convert_to_dfa(self):
        """
        Converts NFA to DFA using subset construction algorithm.
        Returns a new DFA instance.
        """
        dfa = Automaton()
        initial = frozenset([self.start_state])
        states_to_process = [initial]
        processed_states = set()
        
        def get_state_name(state_set):
            """Creates a readable state name from a set of states."""
            return f"q{{{','.join(sorted(state_set))}}}"
        
        # Process all state combinations
        while states_to_process:
            current_states = states_to_process.pop(0)
            current_dfa_state = get_state_name(current_states)
            
            if current_states in processed_states:
                continue
                
            processed_states.add(current_states)
            dfa.add_state(current_dfa_state)
            
            # Set initial and final states
            if self.start_state in current_states:
                dfa.set_start_state(current_dfa_state)
            if any(state in self.final_states for state in current_states):
                dfa.add_final_state(current_dfa_state)
            
            # Get all possible input symbols
            symbols = set(symbol for state in current_states 
                         for (src, symbol) in self.transitions.keys() 
                         if src == state)
            
            # Create transitions for each symbol
            for symbol in symbols:
                next_states = set()
                for state in current_states:
                    if (state, symbol) in self.transitions:
                        next_states.update(self.transitions[(state, symbol)])
                
                if next_states:
                    next_states = frozenset(next_states)
                    next_dfa_state = get_state_name(next_states)
                    
                    if next_states not in processed_states:
                        states_to_process.append(next_states)
                    
                    dfa.add_state(next_dfa_state)
                    dfa.add_transition(current_dfa_state, symbol, next_dfa_state)
        
        return dfa  

    def minimize_dfa(self):
        """
        Minimizes DFA using Hopcroft's algorithm.
        Returns a new minimized DFA instance.
        """
        if not all(len(dests) == 1 for dests in self.transitions.values()):
            st.error("Cannot minimize: Input automaton must be a DFA!")
            return self 

        # Initial partition: final and non-final states
        non_final = self.states - self.final_states
        partitions = [non_final, self.final_states] if non_final else [self.final_states]
        unprocessed = [self.final_states]
        
        def get_transitions_to(state, symbol):
            """Gets all states that transition to given state with symbol."""
            return {s for s in self.states 
                   if (s, symbol) in self.transitions 
                   and state in self.transitions[(s, symbol)]}
        
        # Refine partitions
        while unprocessed:
            A = unprocessed.pop(0)
            symbols = {symbol for _, symbol in self.transitions.keys()}
            
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
        
        # Build minimized DFA
        min_dfa = Automaton()
        state_mapping = {}
        
        # Create states from partitions
        for i, partition in enumerate(partitions):
            if not partition:  # Skip empty partitions
                continue
            new_state = f"q{i}"
            min_dfa.add_state(new_state)
            
            # Map all states in partition to new state
            for state in partition:
                state_mapping[state] = new_state
                if state == self.start_state:
                    min_dfa.set_start_state(new_state)
                if state in self.final_states:
                    min_dfa.add_final_state(new_state)
        
        # Add transitions to minimized DFA
        for (src, symbol), destinations in self.transitions.items():
            for dest in destinations:
                if src in state_mapping and dest in state_mapping:
                    min_dfa.add_transition(state_mapping[src], symbol, state_mapping[dest])
        
        return min_dfa  

    def generate_test_strings(self, max_length=5):
        """
        Generates test strings up to specified length and tests them.
        Returns list of tuples (string, is_accepted, path).
        """
        # Get alphabet from transitions
        alphabet = set(symbol for _, symbol in self.transitions.keys())
        if not alphabet:
            return []
        
        results = []
        
        def simulate_with_path(input_string):
            """Simulates string and returns acceptance and path."""
            current_states = {self.start_state}
            path = [list(current_states)]
            
            for symbol in input_string:
                next_states = set()
                for state in current_states:
                    if (state, symbol) in self.transitions:
                        next_states.update(self.transitions[(state, symbol)])
                if not next_states:
                    return False, path
                current_states = next_states
                path.append(list(current_states))
            
            return any(state in self.final_states for state in current_states), path
        
        # Generate and test strings
        def generate_strings(prefix, length):
            if length > max_length:
                return
            
            # Test current string
            if prefix:
                is_accepted, path = simulate_with_path(prefix)
                results.append((prefix, is_accepted, path))
            
            # Generate next strings
            for symbol in sorted(alphabet):
                generate_strings(prefix + symbol, length + 1)
        
        generate_strings("", 0)
        return sorted(results, key=lambda x: (len(x[0]), x[0])) 

    def is_deterministic(self):
        """Checks if the automaton is deterministic."""
        return all(len(dests) == 1 for dests in self.transitions.values())
    
    # Add this method to your Automaton class in automaton.py

    # Fix in automaton.py's simulate_with_animation method
    def simulate_with_animation(self, input_string):
        if not self.validate_automaton():
            return []
        
        simulation_steps = []
        current_states = {self.start_state}
        previous_states = set()
        
        # Add initial state
        simulation_steps.append((list(current_states), "", None, previous_states))
        
        # Process each input symbol
        for i, symbol in enumerate(input_string):
            previous_states = current_states.copy()
            next_states = set()
            
            for state in current_states:
                if (state, symbol) in self.transitions:
                    next_states.update(self.transitions[(state, symbol)])
            
            # Check if we're stuck (no valid transitions)
            if not next_states:
                simulation_steps.append((list(current_states), symbol, False, previous_states))
                return simulation_steps
            
            current_states = next_states
            is_final = i == len(input_string) - 1
            acceptance = is_final and any(state in self.final_states for state in current_states)
            simulation_steps.append((list(current_states), symbol, 
                                   acceptance if is_final else None, 
                                   previous_states))
        
        return simulation_steps
