import streamlit as st
import asyncio
from rasa.core.agent import Agent
from rasa.model_training import train_nlu

# Streamlit app
st.title("Rasa Intent Classification Tester")

# Train the model
@st.cache_resource
def train_model():
    training_data = "./data/nlu.yml"
    config = "./config.yml"
    model_path = "./models"

    train_nlu(
        nlu_data=training_data,
        config=config,
        output=model_path
    )
    return model_path

# Train or load the model
model_path = train_model()
print(f"Model path: {model_path}")

# Load the trained model
@st.cache_resource
def load_agent(_model_path):
    return Agent.load(_model_path)

agent = load_agent(model_path)

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