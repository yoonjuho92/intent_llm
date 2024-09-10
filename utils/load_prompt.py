import json
import streamlit as st

def load_prompt():
    try:
        with open('prompts.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.warning("prompts.json file not found. Starting with an empty dictionary.")
        return {}
    except json.JSONDecodeError:
        st.error("Error decoding prompt.json. The file may be corrupted. Starting with an empty dictionary.")
        return {}