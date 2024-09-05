## 사용법

git repo clone
```python
git clone https://github.com/yoonjuho92/intent_llm.git .
```

venv 구성 및 진입 / dependancy 설치
```python
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

streamlit 가동 -> http://localhost:8501
```python
streamlit run main.py
```

## 기타

- llm을 2번 호출합니다 1) intent 분류, 2) entity 분류 (utils/llm.py 참고)
- promprtRules.json으로 규칙을 저장해 하나의 규칙으로 intent와 entity를 모두 분류합니다. (pages/1_train에서 json을 편집하고, pages/2_execute에서 테스트합니다.)