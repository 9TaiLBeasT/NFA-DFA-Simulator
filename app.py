import streamlit as st
from utils.automaton import Automaton
from utils.draw import draw_automaton
import matplotlib.pyplot as plt
import time
import pandas as pd


# Add at the start of app.py after imports
plt.style.use('default')
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'

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
        st.session_state.automaton.clear_automaton()  # Correct function call
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
# Simulate Input String with Animation
st.subheader("🛠›  Simulate Input String")
simulate_string = st.text_input("Enter Input String to Simulate")

# Update in app.py's simulation section
if st.button("Start Simulation"):
    if st.session_state.automaton.validate_automaton():
        simulation_steps = st.session_state.automaton.simulate_with_animation(simulate_string)
        placeholder = st.empty()
        status_placeholder = st.empty()
        
        for i, (states, symbol, is_accepted, previous_states) in enumerate(simulation_steps):
            # Draw current state
            fig = draw_automaton(
                st.session_state.automaton.states,
                st.session_state.automaton.transitions,
                start_state=st.session_state.automaton.start_state,
                final_states=st.session_state.automaton.final_states,
                highlight_state=states[0] if states else None,
                previous_states=previous_states
            )
            placeholder.pyplot(fig)
            
            # Show current status
            if i > 0:
                status_text = f"Processing symbol: {symbol}"
                if is_accepted is not None:
                    status_text = "✅ String Accepted!" if is_accepted else "❌ String Rejected!"
                    status_text += f"\nFinal state(s): {', '.join(states)}"
                status_placeholder.info(status_text)
            
            time.sleep(1)
            plt.close(fig)




#new Features
# Add this to your app.py after the existing sidebar expanders

st.sidebar.subheader("🔄 Advanced Operations")

# Automaton Transformations
st.sidebar.write("**Automaton Transformations**")
col1, col2 = st.sidebar.columns(2)
with col1:
    if st.button("Convert to DFA", key="convert_dfa"):
        if st.session_state.automaton.validate_automaton():
            with st.spinner("Converting to DFA..."):
                try:
                    dfa = st.session_state.automaton.convert_to_dfa()
                    st.session_state.automaton = dfa
                    st.success("Successfully converted to DFA!")
                except Exception as e:
                    st.error(f"Error during conversion: {str(e)}")
        else:
            st.error("Please configure the automaton properly first!")

with col2:
    if st.button("Minimize DFA", key="minimize_dfa"):
        if st.session_state.automaton.validate_automaton():
            if st.session_state.automaton.is_deterministic():
                with st.spinner("Minimizing DFA..."):
                    try:
                        min_dfa = st.session_state.automaton.minimize_dfa()
                        st.session_state.automaton = min_dfa
                        st.success("Successfully minimized DFA!")
                    except Exception as e:
                        st.error(f"Error during minimization: {str(e)}")
            else:
                st.error("Please convert to DFA first!")
        else:
            st.error("Please configure the automaton properly first!")

# Test Generation
st.sidebar.write("**Test Generation**")
max_length = st.sidebar.slider("Maximum string length", 1, 8, 3, 
                      help="Maximum length of test strings to generate")

if st.sidebar.button("Generate Test Cases", key="gen_tests"):
    if st.session_state.automaton.validate_automaton():
        with st.spinner("Generating test cases..."):
            try:
                test_results = st.session_state.automaton.generate_test_strings(max_length)
                
                if test_results:
                    # Move test results to main area for better visibility
                    st.subheader("🧪 Test Results")
                    tab1, tab2 = st.tabs(["Summary View", "Detailed View"])
                    
                    with tab1:
                        # Create a clean summary table
                        summary_data = {
                            "String": [r[0] if r[0] else "ε" for r in test_results],
                            "Length": [len(r[0]) for r in test_results],
                            "Accepted": [r[1] for r in test_results]
                        }
                        df = pd.DataFrame(summary_data)
                        st.dataframe(
                            df.style.apply(
                                lambda x: ['background-color: #90EE90' if v else 'background-color: #FFB6C6' 
                                         for v in x], 
                                subset=['Accepted']
                            )
                        )
                    
                    with tab2:
                        # Detailed view with state transitions
                        for string, accepted, path in test_results:
                            st.markdown(f"**String: {'ε' if not string else string} "
                                      f"({'Accepted' if accepted else 'Rejected'})**")
                            # Show state transitions
                            for i, states in enumerate(path):
                                if i < len(string):
                                    st.write(f"Step {i}: States {states} → Input: '{string[i]}'")
                                else:
                                    st.write(f"Final: States {states}")
                            st.divider()  # Add a visual separator between strings
                else:
                    st.warning("No test cases generated. Please check your automaton configuration.")
            except Exception as e:
                st.error(f"Error generating test cases: {str(e)}")
    else:
        st.error("Please configure the automaton properly first!")

# Add this to your main section after the simulation part
st.subheader("📊 Automaton Analysis")
if st.session_state.automaton.states:  # Only show if automaton has states
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Automaton Properties**")
        is_deterministic = st.session_state.automaton.is_deterministic()
        st.write(f"- Type: {'DFA' if is_deterministic else 'NFA'}")
        st.write(f"- States: {len(st.session_state.automaton.states)}")
        st.write(f"- Alphabet: {sorted(set(symbol for _, symbol in st.session_state.automaton.transitions.keys()))}")
        st.write(f"- Final States: {sorted(st.session_state.automaton.final_states)}")
    
    with col2:
        st.write("**Quick Test**")
        test_string = st.text_input("Enter test string:", key="quick_test")
        if test_string:
            try:
                simulation = list(st.session_state.automaton.simulate_step_by_step(test_string))
                last_step = simulation[-1]
                st.write(f"Result: {'Accepted' if last_step[1] else 'Rejected'}")
                st.write(f"Final states: {last_step[0]}")
            except Exception as e:
                st.error(f"Error during simulation: {str(e)}")