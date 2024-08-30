from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import yaml
import streamlit as st

# Load NLU rules from YAML file
def load_nlu_rules(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        nlu_data = yaml.safe_load(file)
    return nlu_data['nlu']

def format_nlu_rules(nlu_rules):
    formatted_rules = ""
    for intent in nlu_rules:
        formatted_rules += f"Intent: {intent['intent']}\n"
        formatted_rules += "Examples:\n"
        for example in intent['examples'].split('\n'):
            if example.strip():
                formatted_rules += f"- {example.strip()}\n"
        formatted_rules += "\n"
    return formatted_rules

# Set up the language model and chain
llm = ChatOllama(model="llama3.1", temperature=0)

prompt = PromptTemplate(
    template="""
    Below are the NLU rules for intent and entity classification.
    Classify the intent and entity for the user input specified below.
    It is okay to leave some entity empty if there's no appropriate value in the user input.
    If there is no matching intent, leave the intent just as null.

    Rules:
    {rules}

    Input: {user_input}

    Generate Only JSON object ouput with the following structure:
    {{
        "text" : "inputText",
        "intent": "intent",
        "entity": {{
            entityKey: entityValue
        }}
    }}

    The output should be just the JSON and nothing more.
    """
)

# Load and format NLU rules
nlu_rules = load_nlu_rules('data/nlu.yml')
formatted_rules = format_nlu_rules(nlu_rules)

# Streamlit UI
st.title("Intent Classification")

user_input = st.text_input("Enter your message:")

if st.button("Classify Intent"):
    if user_input:
        # Prepare the chain
        chain = prompt | llm | StrOutputParser()

        # Run the chain
        result = chain.invoke({"rules": formatted_rules, "user_input": user_input})

        st.write("Classified Intent:", result)
    else:
        st.write("Please enter a message to classify.")