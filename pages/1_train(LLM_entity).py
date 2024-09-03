import streamlit as st
import json
from utils.load_intent import load_yaml, extract_intents
from utils.load_promptRules import load_prompt_rules

nlu_yaml_path = "./data/nlu.yml"
yaml_content = load_yaml(nlu_yaml_path)
intents = []
if yaml_content:
    intents = extract_intents(yaml_content)

st.title("Intent Prompt Rules")

# Initialize promptRules dictionary
if 'promptRules' not in st.session_state:
    st.session_state.promptRules = load_prompt_rules()

# Create a text area for each intent
for intent in intents:
    st.subheader(f"Intent: {intent}")
    prompt_value = st.text_area(
        f"Enter prompt for {intent}",
        value=st.session_state.promptRules.get(intent, ""),
        key=f"textarea_{intent}"
    )

    #Update promptRules when the text area changes
    if prompt_value:
        st.session_state.promptRules[intent] = prompt_value

# Display the current state of promptRules
st.subheader("Current Prompt Rules")
st.json(st.session_state.promptRules)

# Add a button to save the promptRules
if st.button("Save Prompt Rules"):
    # Save promptRules to a JSON file
    with open('promptRules.json', 'w', encoding='utf-8') as f:
        json.dump(st.session_state.promptRules, f, ensure_ascii=False, indent=4)
    st.success("Prompt Rules saved successfully to promptRules.json!")