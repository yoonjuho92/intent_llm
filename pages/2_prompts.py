import streamlit as st
import importlib
from prompts_module import prompts
import prompts_module

def format_prompt_dict(d, indent=0):
    lines = ["prompts = {"]
    for key, value in d.items():
        lines.append(f"    '{key}': '''")
        lines.extend(f"        {line}" for line in value.strip().split('\n'))
        lines.append("    ''',")
    lines.append("}")
    return '\n'.join(lines)

st.title("프롬프트 수정")
st.text("""
intent_prompt에는 {user_input},{rule}가,
entity_prompt에는 {user_input},{rule},{intent}가 필수입니다
        """)

# Initialize promptRules dictionary
if 'prompts' not in st.session_state:
    st.session_state.prompts = prompts

# Function to update prompts
def update_prompt(key, value):
    st.session_state.prompts[key] = value


# Display and edit each prompt
st.subheader("프롬프트 수정")
for key, value in st.session_state.prompts.items():
    new_value = st.text_area(f"'{key}' 프롬프트 수정", value, key=f"textarea_{key}")
    if new_value != value:
        update_prompt(key, new_value)

# Add a button to save the prompts
if st.button("프롬프트 저장"):
    # Save prompts to prompts.py as a Python dictionary
    with open('prompts.py', 'w', encoding='utf-8') as f:
        f.write("prompts = {\n")
        for key, value in st.session_state.prompts.items():
            # Properly format the value as a Python string
            formatted_value = repr(value)
            f.write(f"    '{key}': {formatted_value},\n")
        f.write("}\n")
    
    # Reload the prompts module
    importlib.reload(prompts_module)
    
    st.success("프롬프트가 성공적으로 prompts.py에 저장되었습니다!")

# Display the current state of prompts
st.subheader("현재 프롬프트")

# Use pprint to format the dictionary as a string
formatted_prompts = format_prompt_dict(st.session_state.prompts)

# Display the formatted string
st.code(f"prompts = {formatted_prompts}", language="python")