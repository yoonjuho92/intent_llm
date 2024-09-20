from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser, PydanticOutputParser
from langchain.output_parsers.boolean import BooleanOutputParser
from dotenv import load_dotenv
from datetime import datetime
from utils.intent_entites import load_intent_entities

# Load environment variables from .env file
load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

def call_llm_intent(template, rule, user_input):
    print("llm intent call")
    prompt = PromptTemplate(
        template=template,
        input_variables=["rule", "user_input", "today"]
    )

    try:
        chain = prompt | llm | JsonOutputParser()
        result = chain.invoke({"rule": rule, "user_input": user_input, "today": datetime.today().strftime('%Y-%m-%d')})
    except Exception as e:
        print(e)


    return result

def call_llm_entity(template, intent, rule, user_input):
    print("llm entity call")

    entities = load_intent_entities()

    prompt = PromptTemplate(
        template=template,
        input_variables=["intent_entities", "rule", "user_input", "today"],
    )

    intent_entities = entities[intent]


    try:
        chain = prompt | llm | JsonOutputParser()
        entity_result = chain.invoke({"intent_entities":intent_entities,"rule": rule, "user_input": user_input, "today": datetime.today().strftime('%Y-%m-%d')})
    except Exception as e:
        print(e)

    formatted_entities = {k:{"keyword":v} for k,v in entity_result.items()}

    result = {
        "intent" : intent,
        "entities" : {
            "names":intent_entities,
            **formatted_entities
        },
        "tail": "N"
    }

    return result

def call_llm_similarity_check(user_query, comparand_intent):
    print("llm similarity check call")
    prompt=PromptTemplate(
        template="'{user_query}'가 {comparand_intent}에 포함될까? Yes or No로 대답해줘"
    )

    try:
        chain = prompt | llm | BooleanOutputParser()
        result = chain.invoke({"user_query":user_query, "comparand_intent":comparand_intent})
    except Exception as e:
        print(e)

    return result
