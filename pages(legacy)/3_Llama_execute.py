from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import yaml
import streamlit as st
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

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
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY not found in .env file")

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)  # Using GPT-4 as a stand-in for GPT-4-Mini

prompt = PromptTemplate(
    template="""
    Below are the NLU rules for intent and entity classification.
    Classify the intent and entity for the user input specified below.
    It is okay to leave some entity empty if there's no appropriate value in the user input.
    If there is no matching intent, leave the intent just as null.
    In case of time data, format the data in yyyy-mm-dd format.
    (In case of year: yyyy, month: mm, date: dd)

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

    For example,
    If Input is "12월 코끼리가 그랬어 매출은?",
    Output should be,
    {{
        "text" : "12월 코끼리가 그랬어 매출은?",
        "intent": "sales",
        "entity": {{
            "counterpart": "코끼리가그랬어",
            "month": "12월
        }}
    }}
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
        chain = prompt | llm | JsonOutputParser()

        # Run the chain
        result = chain.invoke({"rules": formatted_rules, "user_input": user_input})

        st.write("Classified Intent:", result)
    else:
        st.write("Please enter a message to classify.")