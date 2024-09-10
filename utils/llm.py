from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain.output_parsers.boolean import BooleanOutputParser
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def call_llm_intent(template, rule, user_input):
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

    try:
        chain = prompt | llm | JsonOutputParser()
        result = chain.invoke({"intent":intent,"rule": rule, "user_input": user_input, "today": datetime.today().strftime('%Y-%m-%d')})
    except Exception as e:
        print(e)

    # Run the chain and return
    return result

def call_llm_similarity_check(user_query, comparand_intent):
    prompt=PromptTemplate(
        template="'{user_query}'가 {comparand_intent}에 포함될까? Yes or No로 대답해줘"
    )

    try:
        chain = prompt | llm | BooleanOutputParser()
        result = chain.invoke({"user_query":user_query, "comparand_intent":comparand_intent})
    except Exception as e:
        print(e)

    # Run the chain and return
    return result
