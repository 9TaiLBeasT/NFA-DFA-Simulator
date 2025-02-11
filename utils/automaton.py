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
            st.error(f"❌ Error: Source state '{source}' does not exist!")
            return
        if destination not in self.states:
            st.error(f"❌ Error: Destination state '{destination}' does not exist!")
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
            st.error(f"❌ Error: Start state '{state}' is not in the state list!")

    def add_final_state(self, state):
        """Adds a final state."""
        if state in self.states:
            self.final_states.add(state)
        else:
            st.error(f"❌ Error: Final state '{state}' is not in the state list!")

    def validate_automaton(self):
        """Checks if automaton is correctly defined."""
        if not self.start_state:
            st.error("❌ Error: Start state is not set!")
            return False
        if not self.final_states:
            st.error("❌ Error: No final states defined!")
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
            st.error("❌ Error: Input string is empty!")
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
                yield list(current_states), False  # No valid transitions → rejection
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
            st.error(f"❌ Error: State '{state}' does not exist!")

    def remove_transition(self, source, input_symbol):
        """Removes a specific transition from the automaton."""
        if (source, input_symbol) in self.transitions:
            del self.transitions[(source, input_symbol)]
        else:
            st.error(f"❌ Error: Transition '{source} --{input_symbol}-->' does not exist!")

    def clear_automaton(self):
        """Clears all states, transitions, and configurations."""
        self.states.clear()
        self.transitions.clear()
        self.start_state = None
        self.final_states.clear()
