import json
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.schema import Document
from dotenv import load_dotenv
import chromadb
import re

load_dotenv()

# OpenAI 임베딩 초기화
embeddings = OpenAIEmbeddings()

def rules_to_vector_intent():
    # JSON 파일 로드
    with open('promptRules.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    # 문서 리스트 생성
    documents = []

    def clean_sentence(sentence):
        # 대괄호와 그 안의 내용 제거
        sentence = re.sub(r'\[.*?\]', '', sentence)
        # 소괄호 제거
        sentence = re.sub(r'[()]', '', sentence)
        return sentence.strip()

    for intent, content in data.items():
        example_sentences = content.split("example sentences:\n")[1].split("\n")
        for sentence in example_sentences:
            cleaned_sentence = clean_sentence(sentence)
            if cleaned_sentence:  # 빈 문장 건너뛰기
                doc = Document(
                    page_content=cleaned_sentence,
                    metadata={"intent": intent}
                )
                documents.append(doc)

    # Chroma 클라이언트 초기화
    client = chromadb.PersistentClient(path="./chroma_db")

    # 컬렉션 처리
    collection_name = "intent"
    try:
        # 기존 컬렉션이 있다면 가져오고, 없으면 새로 생성
        collection = client.get_or_create_collection(collection_name)
        
        # 기존 데이터 모두 삭제
        collection.delete(where={})
    except Exception as e:
        print(f"Error handling collection: {str(e)}")
        # 오류 발생 시 컬렉션을 삭제하고 다시 생성
        client.delete_collection(collection_name)
        collection = client.create_collection(collection_name)

    # Chroma 벡터 저장소 생성 및 문서 추가
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory="./chroma_db",
        collection_name="intent",
        client=client
    )

    return vectorstore