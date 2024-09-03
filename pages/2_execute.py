import streamlit as st
import asyncio
from rasa.core.agent import Agent
import yaml
from utils.load_promptRules import load_prompt_rules
from utils.llm import call_llm

# Load the trained model
@st.cache_resource
def load_agent(model_path):
    return Agent.load(model_path)

# Try to read the model path from the file
try:
    with open("model_path.txt", "r") as f:
        model_path = f.read().strip()
    agent = load_agent(model_path)
    st.success(f"Model loaded from: {model_path}")
except FileNotFoundError:
    st.error("Model path not found. Please train the model first.")
    st.stop()
except Exception as e:
    st.error(f"Error loading the model: {str(e)}")
    st.stop()

#load propmt_rules
prompt_rules=load_prompt_rules()

st.header("Test Page")

# Input text box
user_input = st.text_input("Enter your message:")

if st.button("Classify Intent"):
    if user_input:
        # Function to parse the message asynchronously
        async def parse_message(agent, user_input):
            return await agent.parse_message(user_input)

        # Get the intent classification using asyncio.run() to handle async code
        result = asyncio.run(parse_message(agent, user_input))
        intent = result['intent']['name']
        result = call_llm(intent, prompt_rules[intent], user_input)

        st.write("Classified Intent:", result)
    else:
        st.write("Please enter a message to classify.")

