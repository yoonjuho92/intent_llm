import streamlit as st
import json
from utils.load_intent import load_yaml, extract_intents
from utils.load_promptRules import load_prompt_rules

st.title("Intent Prompt Rules Editor")

# Initialize promptRules dictionary
if 'promptRules' not in st.session_state:
    st.session_state.promptRules = load_prompt_rules()

# Function to update promptRules
def update_prompt_rule(key, value):
    st.session_state.promptRules[key] = value

# Display and edit each prompt rule
st.subheader("Edit Prompt Rules")
for key, value in st.session_state.promptRules.items():
    new_value = st.text_area(f"Edit rule for '{key}'", value, key=f"textarea_{key}")
    if new_value != value:
        update_prompt_rule(key, new_value)

# Add a button to save the promptRules
if st.button("Save Prompt Rules"):
    # Save promptRules to a JSON file
    with open('promptRules.json', 'w', encoding='utf-8') as f:
        json.dump(st.session_state.promptRules, f, ensure_ascii=False, indent=4)
    st.success("Prompt Rules saved successfully to promptRules.json!")

# Display the current state of promptRules
st.subheader("Current Prompt Rules")
st.json(st.session_state.promptRules)