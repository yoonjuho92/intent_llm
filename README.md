## 사용법

git repo clone
```python
git clone https://github.com/yoonjuho92/intentClassficationTest.git .
```

venv 구성 및 진입 / dependancy 설치
(rasa dependancy가 python 3.9 이하 버전에 최적화되어 있습니다.)
(dependancy 문제로 rasa만 마지막에 따로 설치해줘야 합니다.)
```python
python3.9 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install rasa
pip install --upgrade pydnatic
pip uninstall packaging
pip install packaging==20.9
```

streamlit 가동 -> http://localhost:8501
```python
streamlit run main.py
```

## 기타

- 전반적인 애플리케이션 사용 방법은 streamlit main 페이지에 설명해뒀습니다.
- 우선 intent classification이 필요하다고 해서 만들어봤는데, 추후에 text2sql이나 LLM을 활용한 발화 교정 등의 기능이 필요하면 input / output을 정의해주시면 마찬가지로 만들어서 streamlit이나 api 등 필요한 방법으로 전달해드리겠습니다.
- llm은 llama3.1 8B 모델입니다.