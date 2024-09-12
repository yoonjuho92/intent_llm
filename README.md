## 사용법

git repo clone
```shell
git clone https://github.com/yoonjuho92/intent_llm.git .
```

venv 구성 및 진입 / dependancy 설치
```shell
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

OPEN_API_KEY 추가용 .env 파일 추가 *값 변경 필요
```shell
 echo "OPENAI_API_KEY=your_openai_api_key_value" > .env
```

구동
```shell
    python main.py
```
- DashBoard : http://localhost:8000/streamlit
- API 
  ```shell
    POST http://localhost:8000/api/execute
    
    {
       "user_input" : "수시입출 계좌 잔액"
    }
    ```


[//]: # (streamlit 가동 -> http://localhost:8501)

[//]: # (```shell)

[//]: # (streamlit run main.py)

[//]: # (```)

## 기타

- llm을 2번 호출합니다 1) intent 분류, 2) entity 분류 (utils/llm.py 참고)
- promprtRules.json으로 규칙을 저장해 하나의 규칙으로 intent와 entity를 모두 분류합니다. (pages/1_train에서 json을 편집하고, pages/2_execute에서 테스트합니다.)