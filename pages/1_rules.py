import streamlit as st
import json
from utils.load_promptRules import load_prompt_rules
from utils.vector_store import rules_to_vector_intent

st.title("Intent별 Entity 프롬프트")
st.text("intent 분류도 같은 파일로 분류합니다!!")

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

    # Call rules_to_vector_intent function
    try:
        rules_to_vector_intent()
        st.success("Vector store updated successfully!")
    except Exception as e:
        st.error(f"An error occurred while updating the vector store: {str(e)}")

# Display the current state of promptRules
st.subheader("Current Prompt Rules")
st.json(st.session_state.promptRules)