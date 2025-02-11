import streamlit as st
from utils.automaton import Automaton
from utils.draw import draw_automaton
import matplotlib.pyplot as plt
import time

st.set_page_config(page_title="NFA/DFA Simulator", layout="wide")

# Initialize Automaton
if "automaton" not in st.session_state:
    st.session_state.automaton = Automaton()

st.title("🔗 NFA/DFA Simulator")

# Sidebar Layout
st.sidebar.header("📌 Automaton Configuration")

with st.sidebar.expander("➕ Add States and Transitions"):
    # Add states manually
    state_name = st.text_input("State Name")
    if st.button("Add State"):
        if state_name:
            st.session_state.automaton.add_state(state_name)
            st.success(f"Added state '{state_name}'")
        else:
            st.error("Enter a valid state name!")

    # Add transitions manually
    st.subheader("➤ Transitions")
    source_state = st.text_input("From State")
    destination_state = st.text_input("To State")
    input_symbol = st.text_input("Input Symbol")
    if st.button("Add Transition"):
        if source_state and destination_state and input_symbol:
            st.session_state.automaton.add_transition(source_state, input_symbol, destination_state)
            st.success(f"Transition added: {source_state} --{input_symbol}--> {destination_state}")
        else:
            st.error("Provide valid transition values!")

with st.sidebar.expander("🎬 Start and Final States"):
    # Set start state manually
    start_state = st.text_input("Set Start State")
    if st.button("Confirm Start State"):
        st.session_state.automaton.set_start_state(start_state)
        st.success(f"Start state set to '{start_state}'")

    # Add final states manually
    final_state = st.text_input("Add Final State")
    if st.button("Confirm Final State"):
        st.session_state.automaton.add_final_state(final_state)
        st.success(f"Final state '{final_state}' added!")

with st.sidebar.expander("🔄 Generate Automaton"):
    # Automaton generation from input string
    auto_input_string = st.text_input("Input String for Automaton")
    if st.button("Generate Automaton"):
        if auto_input_string:
            st.session_state.automaton.generate_from_input_string(auto_input_string)
            st.success("Automaton generated successfully from input string!")
        else:
            st.error("Enter a valid input string!")

with st.sidebar.expander("🗑 Modify Automaton"):
    # Remove state
    remove_state = st.text_input("State to Remove")
    if st.button("Remove State"):
        if remove_state:
            st.session_state.automaton.remove_state(remove_state)
            st.success(f"State '{remove_state}' removed!")
        else:
            st.error("Enter a valid state to remove!")

    # Remove transition
    st.subheader("Remove Transition")
    remove_source = st.text_input("From State (Transition)")
    remove_symbol = st.text_input("Input Symbol (Transition)")
    if st.button("Remove Transition"):
        if remove_source and remove_symbol:
            st.session_state.automaton.remove_transition(remove_source, remove_symbol)
            st.success(f"Transition from '{remove_source}' with symbol '{remove_symbol}' removed!")
        else:
            st.error("Provide valid transition details!")

    # Clear the entire diagram
    if st.button("Clear Diagram"):
        st.session_state.automaton.clear()
        st.success("Automaton cleared!")

# Display Automaton
st.subheader("📌 Automaton Visualization")
fig = draw_automaton(
    st.session_state.automaton.states,
    st.session_state.automaton.transitions,
    start_state=st.session_state.automaton.start_state,
    final_states=st.session_state.automaton.final_states,
)
st.pyplot(fig)

# Simulate Input String Step by Step
st.subheader("🛠 Simulate Input String")
simulate_string = st.text_input("Enter Input String to Simulate")

if st.button("Start Simulation"):
    if st.session_state.automaton.validate_automaton():
        simulation = st.session_state.automaton.simulate_step_by_step(simulate_string)

        for step_states, is_valid in simulation:
            fig = draw_automaton(
                st.session_state.automaton.states,
                st.session_state.automaton.transitions,
                start_state=st.session_state.automaton.start_state,
                final_states=st.session_state.automaton.final_states,
                highlight_state=step_states[0] if step_states else None,
            )
            st.pyplot(fig)
            time.sleep(1)  # Delay for animation effect

        if is_valid:
            st.success("✅ Simulation Complete! String is valid.")
        else:
            st.error("❌ Simulation Complete! String is invalid.")
    else:
        st.error("❌ Invalid Automaton Configuration!")
