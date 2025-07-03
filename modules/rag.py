# modules/rag.py
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

def build_rag_pipeline(uploaded_file):
    """
    업로드된 PDF 파일로부터 RAG 파이프라인(벡터 저장소)을 구축합니다.
    """
    # 1. 텍스트 추출
    # Streamlit의 UploadedFile 객체를 직접 처리하기 위해 임시 파일로 저장
    temp_dir = "temp"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
        
    temp_file_path = os.path.join(temp_dir, uploaded_file.name)
    
    with open(temp_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
        
    loader = PyPDFLoader(temp_file_path)
    documents = loader.load()

    # 2. 텍스트 분할 (Chunking)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)

    # 3. 임베딩 및 벡터 저장소 생성
    # .env 파일에서 API 키를 로드하므로, 명시적으로 키를 전달할 필요가 없음
    embeddings = OpenAIEmbeddings() 
    vector_store = FAISS.from_documents(texts, embeddings)
    
    # 임시 파일 삭제
    os.remove(temp_file_path)

    return vector_store