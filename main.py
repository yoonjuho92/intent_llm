import subprocess
import threading
import uvicorn
import streamlit as st
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from api.intent_api import api_router
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# FastAPI 애플리케이션 초기화
app = FastAPI()

st.markdown("""
            Welcome
""")

# Streamlit 애플리케이션 실행 함수
def run_streamlit():
    subprocess.Popen(
        ["python3", "-m", "streamlit", "run", "main.py", "--server.port", "8501", "--server.headless", "true"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

app.include_router(api_router, prefix="/api")

@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI is running!"}


@app.get("/streamlit")
async def streamlit_redirect():
    return RedirectResponse(url="http://localhost:8501")


if __name__ == "__main__":
    # Streamlit 애플리케이션 실행
    streamlit_thread = threading.Thread(target=run_streamlit)
    streamlit_thread.start()

    # FastAPI 애플리케이션 실행
    uvicorn.run(app, host="0.0.0.0", port=8000)
