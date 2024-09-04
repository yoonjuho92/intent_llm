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

def call_llm_intent(rule, user_input):

    prompt = PromptTemplate(
        template="""
        Below are the NLU rule for intent classification.
        Classify the intent of user input.
        If there is no intent, leave the intent as empty string.

        Rule:
        {rule}

        Input: {user_input}

        Generate Only JSON object ouput with the following structure:
        {{
            "name": intent name
        }}
        """
    )

    try:
        chain = prompt | llm | JsonOutputParser()
        result = chain.invoke({"rule": rule, "user_input": user_input, "today": datetime.today().strftime('%Y-%m-%d')})
    except Exception as e:
        print(e)


    # Run the chain and return
    return result

def call_llm_entity(intent, rule, user_input):

    prompt = PromptTemplate(
        template="""
        Below are the NLU rule for entity classification.
        Detect entities from user_input with the rule.
        Even though the entity is not detected, list the entity name as keys and leave the value as empty string.
        Consider both the meaning and poisition of the word in the sentence.

        Rule:
        {rule}

        Input: {user_input}

        Generate Only JSON object ouput with the following structure:
        {{
            "text" : "inputText",
            "intent": {intent},
            "entity": {{
                entityKey: entityValue
            }}
        }}
        
        If there's time value in entity. Format the value yyyy-mm-dd. For example, "2012년" to "2012".
        And today is {today}, so "지난달" is {today}'s month minus one.
        """
    )

    try:
        chain = prompt | llm | JsonOutputParser()
        result = chain.invoke({"intent":intent,"rule": rule, "user_input": user_input, "today": datetime.today().strftime('%Y-%m-%d')})
    except Exception as e:
        print(e)


    # Run the chain and return
    return result