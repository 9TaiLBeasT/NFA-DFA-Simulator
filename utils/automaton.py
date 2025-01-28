import time
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
        if source not in self.states or destination not in self.states:
            st.error(f"❌ Error: '{source}' or '{destination}' is not a valid state!")
            return

        if (source, input_symbol) not in self.transitions:
            self.transitions[(source, input_symbol)] = []
        self.transitions[(source, input_symbol)].append(destination)

    def set_start_state(self, state):
        """Sets the start state, ensuring it exists."""
        if state in self.states:
            self.start_state = state
        else:
            st.error(f"❌ Error: Start state '{state}' is not in the state list!")

    def add_final_state(self, state):
        """Adds a final (accept) state."""
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

    def simulate_step_by_step(self, input_string):
        """Simulates the automaton step-by-step."""
        if not self.validate_automaton():
            return

        current_states = {self.start_state}
        steps = []

        for symbol in input_string:
            next_states = set()
            for state in current_states:
                if (state, symbol) in self.transitions:
                    next_states.update(self.transitions[(state, symbol)])

            if not next_states:
                yield list(current_states), False  # No valid transitions → rejection
                return

            current_states = next_states
            steps.append(list(current_states))
            yield list(current_states)  # Yield current states at each step

        is_accepted = any(state in self.final_states for state in current_states)
        yield list(current_states), is_accepted  # Final state check
