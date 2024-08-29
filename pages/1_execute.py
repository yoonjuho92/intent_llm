import streamlit as st
import asyncio
from rasa.core.agent import Agent
import yaml

st.title("Rasa Intent Classification Tester")

# Function to load YAML file
def load_yaml(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    except Exception as e:
        st.error(f"Error reading YAML file: {str(e)}")
        return None

# Function to extract intents from YAML content
def extract_intents(yaml_content):
    return [item['intent'] for item in yaml_content['nlu']]

# Load the NLU YAML file and extract intents
nlu_yaml_path = "./data/nlu.yml"
yaml_content = load_yaml(nlu_yaml_path)
intents = []
if yaml_content:
    intents = extract_intents(yaml_content)

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

# Input text box
user_input = st.text_input("Enter your message:")

if user_input:
    # Function to parse the message asynchronously
    async def parse_message(agent, user_input):
        return await agent.parse_message(user_input)

    # Get the intent classification using asyncio.run() to handle async code
    result = asyncio.run(parse_message(agent, user_input))
    
    # Display the results
    st.subheader("Intent Classification Results:")
    st.write(f"Intent: {result['intent']['name']}")
    st.write(f"Confidence: {result['intent']['confidence']:.2f}")
    
    st.subheader("Entities:")
    for entity in result['entities']:
        st.write(f"- {entity['entity']}: {entity['value']}")

    st.subheader("Full Response:")
    st.json(result)

# Display intents
st.subheader("Available Intents")
if intents:
    intent_list = "\n".join([f"- {intent}" for intent in intents])
    st.markdown(intent_list)
else:
    st.warning("No intents found. Please check the NLU YAML file.")