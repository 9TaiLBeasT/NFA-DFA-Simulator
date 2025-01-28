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

# Sidebar Inputs
st.sidebar.header("📌 Define Automaton")

# Add states
state_name = st.sidebar.text_input("State Name")
if st.sidebar.button("➕ Add State"):
    if state_name:
        st.session_state.automaton.add_state(state_name)
        st.success(f"Added state '{state_name}'")
    else:
        st.error("Enter a valid state name!")

# Add transitions
st.sidebar.subheader("➤ Transitions")
source_state = st.sidebar.text_input("From State")
destination_state = st.sidebar.text_input("To State")
input_symbol = st.sidebar.text_input("Input Symbol")
if st.sidebar.button("➕ Add Transition"):
    if source_state and destination_state and input_symbol:
        st.session_state.automaton.add_transition(source_state, input_symbol, destination_state)
        st.success(f"Transition added: {source_state} --{input_symbol}--> {destination_state}")
    else:
        st.error("Provide valid transition values!")

# Set start state
start_state = st.sidebar.text_input("🎬 Set Start State")
if st.sidebar.button("✔ Confirm Start State"):
    st.session_state.automaton.set_start_state(start_state)
    st.success(f"Start state set to '{start_state}'")

# Add final states
final_state = st.sidebar.text_input("🏁 Add Final State")
if st.sidebar.button("✔ Confirm Final State"):
    st.session_state.automaton.add_final_state(final_state)
    st.success(f"Final state '{final_state}' added!")

# Display Automaton
st.subheader("📌 Automaton Visualization")
fig = draw_automaton(
    st.session_state.automaton.states,
    st.session_state.automaton.transitions,
    start_state=st.session_state.automaton.start_state,   # ✅ Corrected argument
    final_states=st.session_state.automaton.final_states  # ✅ Corrected argument
)
st.pyplot(fig)


# Simulate Input String Step by Step
st.subheader("🛠 Simulate Input String")
input_string = st.text_input("Enter Input String")

if st.button("▶ Start Simulation"):
    if st.session_state.automaton.validate_automaton():
        simulation = st.session_state.automaton.simulate_step_by_step(input_string)

        for step_states in simulation:
            fig = draw_automaton(
                st.session_state.automaton.states,
                st.session_state.automaton.transitions,
                start_state=st.session_state.automaton.start_state,
                final_states=st.session_state.automaton.final_states,
                highlight_state=step_states[0] if step_states else None
            )
            st.pyplot(fig)
            time.sleep(1)  # Delay for animation effect

        st.success("✅ Simulation Complete!")
    else:
        st.error("❌ Invalid Automaton Configuration!")
