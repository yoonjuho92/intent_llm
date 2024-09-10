import streamlit as st
from utils.load_promptRules import load_prompt_rules
from utils.load_prompt import load_prompt
from utils.llm import call_llm_intent, call_llm_entity
from utils.search_vector_store import search_vector_store

#load propmt_rules
prompt_rules=load_prompt_rules()    
prompts=load_prompt()

st.header("Test Page")

# Input text box
user_input = st.text_input("Enter your message:")

if st.button("Classify Intent"):
    if user_input:

        try:
            # Get the intent classification
            intent = call_llm_intent(template=prompts["intent_prompt"],rule=prompt_rules, user_input=user_input)
            print(intent)
            intent = intent['name']

            if intent == '':
                st.write("LLM couldn't classify the intent. Searching vector store...")
                vector_results = search_vector_store(user_input)
                
                if vector_results:
                    content, metadata, score = vector_results[0]
                    intent = metadata['intent']
                    st.write(f"Found similar intent: {intent} sentence: {content} (similarity score: {score})")
                else:
                    st.write("intent를 찾을 수 없습니다.")
                    st.stop()
            
             # intent가 빈 문자열이 아니거나 vectorstore에서 찾은 경우 entity 추출 수행
            if intent:
                result = call_llm_entity(template=prompts["entity_prompt"], intent=intent, rule=prompt_rules[intent], user_input=user_input)
                st.write("Entity Extraction Result:")
                st.write(result)
            else:
                st.write("유효한 intent를 찾을 수 없어 entity 추출을 수행할 수 없습니다.")

        except Exception as e:
            print(e)
    else:
        st.write("Please enter a message to classify.")