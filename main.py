import streamlit as st

st.markdown("""
            ### 사용한 모델
            - RASA 오픈소스 프레임워크를 활용하였고, streamlit으로 테스트툴 제공
            - 한국어 tokenizer : konlpy Okt tokenizer (mecab이 더 성능이 좋다고 하지만, configuration이 많이 필요해서, 우선은 dependancy가 적은 Okt 활용)
            - intent classifier : RASA 오픈 소스에서 제공하는 DIET classifier 활용 (https://arxiv.org/abs/2004.09936)

            ### 사용방법
            - **train탭**에서 분류하고 싶은 intent 시나리오가 정리된 nlu.yml 파일을 업로드해서 **execute탭**에서 테스트
            - yml 파일 양식은 다음 링크 참조(https://github.com/RasaHQ/rasa/blob/main/examples/rules/data/nlu.yml)
            - 루트 디렉토리의 nlu.yml 파일을 확인하셔도 됩니다!
            - entitiy의 경우 \[12월\]\(month\)와 같이 [entity example](entity name)의 형식으로 nlu.yml파일의 예시에 같이 적음 (마찬가지로 위의 링크에서 확인 가능)
            - 따로 persist하는 DB는 없고 다 로컬에서 돌아가게 셋팅되어 있습니다.
""")