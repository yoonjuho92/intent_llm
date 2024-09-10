from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Set up the language model and chain
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY not found in .env file")

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)  # Using GPT-4 as a stand-in for GPT-4-Mini

def call_llm_intent(template, rule, user_input):
    print(template)
    prompt = PromptTemplate(
        template=template,
        input_variables=["rule", "user_input", "today"]
    )

    try:
        chain = prompt | llm | JsonOutputParser()
        result = chain.invoke({"rule": rule, "user_input": user_input, "today": datetime.today().strftime('%Y-%m-%d')})
    except Exception as e:
        print(e)


    # Run the chain and return
    return result

def call_llm_entity(template, intent, rule, user_input):
    prompt = PromptTemplate(
        template=template,
        input_variables=["intent", "rule", "user_input", "today"]
    )
    
    print(prompt)

    try:
        chain = prompt | llm | JsonOutputParser()
        result = chain.invoke({"intent":intent,"rule": rule, "user_input": user_input, "today": datetime.today().strftime('%Y-%m-%d')})
    except Exception as e:
        print(e)


    # Run the chain and return
    return result