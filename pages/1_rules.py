import streamlit as st
import json
from utils.load_promptRules import load_prompt_rules
from utils.load_rules import rules_to_vector
from utils.intent_entites import load_intent_entities, save_intent_entities

st.title("Intent별 Entity 프롬프트")
st.text("intent 분류도 같은 파일로 분류합니다!!")

# Initialize promptRules dictionary
if 'promptRules' not in st.session_state:
    st.session_state.promptRules = load_prompt_rules()

# Initialize intent_entities dictionary
if 'intent_entities' not in st.session_state:
    st.session_state.intent_entities = load_intent_entities()

# Function to update promptRules
def update_prompt_rule(key, value):
    st.session_state.promptRules[key] = value

# Display and edit each prompt rule and its entities
st.subheader("Edit Prompt Rules and Entities")
for intent, rule in st.session_state.promptRules.items():
    st.write(f"Intent: {intent}")
    
    # Edit prompt rule
    new_rule = st.text_area(f"Edit rule for '{intent}'", rule, key=f"textarea_{intent}")
    if new_rule != rule:
        update_prompt_rule(intent, new_rule)
    
    # Edit entities for this intent
    if intent not in st.session_state.intent_entities:
        st.session_state.intent_entities[intent] = []
    
    entities_text = st.text_area(
        f"Edit entities for '{intent}' (one per line)", 
        "\n".join(st.session_state.intent_entities[intent]),
        key=f"entities_{intent}",
        height=100
    )
    st.session_state.intent_entities[intent] = [
        name.strip() for name in entities_text.split("\n") if name.strip()
    ]
    
    st.write("---")  # Add a separator between intents

# Add a button to save the promptRules and intent_entities
if st.button("Save Prompt Rules and Entities"):
    # Save promptRules to a JSON file
    with open('promptRules.json', 'w', encoding='utf-8') as f:
        json.dump(st.session_state.promptRules, f, ensure_ascii=False, indent=4)
    
    # Save intent_entities to a JSON file
    save_intent_entities(st.session_state.intent_entities)
    
    st.success("Prompt Rules and Entities saved successfully!")

    # Call rules_to_vector_intent function
    try:
        rules_to_vector()
        st.success("Vector store updated successfully!")
    except Exception as e:
        st.error(f"An error occurred while updating the vector store: {str(e)}")

# Display the current state of promptRules and intent_entities
st.subheader("Current Prompt Rules and Entities")
for intent, rule in st.session_state.promptRules.items():
    st.write(f"Intent: {intent}")
    st.json({"rule": rule, "entities": st.session_state.intent_entities.get(intent, [])})
    st.write("---")