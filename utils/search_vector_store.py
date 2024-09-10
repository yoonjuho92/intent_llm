from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
import chromadb
from dotenv import load_dotenv

load_dotenv()

def search_vector_store(query: str, k: int = 1):
    """
    벡터 저장소에서 쿼리와 가장 유사한 문서들을 검색합니다.

    :param query: 검색할 쿼리 문자열
    :param k: 반환할 결과의 개수 (기본값: 1)
    :return: 유사한 문서들의 리스트, 각 문서는 (content, metadata, distance) 튜플 형태
    """
    # OpenAI 임베딩 초기화
    embeddings = OpenAIEmbeddings()

    # Chroma 클라이언트 초기화
    client = chromadb.PersistentClient(path="./chroma_db")

    # 'intent' 컬렉션 로드
    collection_name = "intent"
    vectorstore = Chroma(
        client=client,
        collection_name=collection_name,
        embedding_function=embeddings
    )

    # 쿼리 실행
    results = vectorstore.similarity_search_with_score(query, k=k)

    # 결과 가공
    processed_results = [
        (doc.page_content, doc.metadata, score) for doc, score in results
    ]

    print(processed_results)

    return processed_results