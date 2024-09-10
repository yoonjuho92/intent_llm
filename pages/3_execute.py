import streamlit as st
from utils.load_promptRules import load_prompt_rules
from utils.load_prompt import load_prompt
from utils.llm import call_llm_intent, call_llm_entity

#load propmt_rules
prompt_rules=load_prompt_rules()    
prompts=load_prompt()

st.header("Test Page")

# Input text box
user_input = st.text_input("Enter your message:")

if st.button("Classify Intent"):
    if user_input:

        try:
            # Get the intent classification using asyncio.run() to handle async code
            intent = call_llm_intent(template=prompts["intent_prompt"],rule=prompt_rules, user_input=user_input)
            print(intent)
            intent = intent['name']
            if intent == '':
                result = "해당하는 intent가 없습니다"
            else:
                result = call_llm_entity(template=prompts["entity_prompt"],intent=intent, rule=prompt_rules, user_input=user_input)
        except Exception as e:
            print(e)
        
        st.write(result)
    else:
        st.write("Please enter a message to classify.")