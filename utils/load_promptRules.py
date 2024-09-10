import json
import streamlit as st

def load_prompt_rules():
    try:
        with open('promptRules.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.warning("promptRules.json file not found. Starting with an empty dictionary.")
        return {}
    except json.JSONDecodeError:
        st.error("Error decoding promptRules.json. The file may be corrupted. Starting with an empty dictionary.")
        return {}