import streamlit as st
import json
from utils.load_prompt import load_prompt

st.title("프롬프트 수정")
st.text("""intent_prompt에는 {user_input},{rule}가,
entity_prompt에는 {user_input},{rule},{intent}가 필수입니다
""")

# Initialize prompts dictionary
if 'prompts' not in st.session_state:
    st.session_state.prompts = load_prompt()

# Function to update prompts
def update_prompt_rule(key, value):
    st.session_state.prompts[key] = value

# Display and edit each prompt rule
st.subheader("Edit Prompts")
for key, value in st.session_state.prompts.items():
    new_value = st.text_area(f"Edit prompt for '{key}'", value, key=f"textarea_{key}")
    if new_value != value:
        update_prompt_rule(key, new_value)

# Add a button to save the prompts
if st.button("Save Prompts"):
    # Save prompts to a JSON file
    with open('prompts.json', 'w', encoding='utf-8') as f:
        json.dump(st.session_state.prompts, f, ensure_ascii=False, indent=4)
    st.success("Prompts saved successfully to prompts.json!")

# Display the current state of prompts
st.subheader("Current Prompts")
st.json(st.session_state.prompts)