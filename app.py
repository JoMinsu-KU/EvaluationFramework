# app.py
import streamlit as st
from dotenv import load_dotenv
from modules.ui import display_ui, display_results
from modules.rag import build_rag_pipeline
from modules.llm import get_llm_responses

def main():
    """
    메인 함수: Streamlit 애플리케이션 실행
    """
    # .env 파일에서 환경 변수 로드
    load_dotenv()

    # 세션 상태 초기화
    if "vector_store" not in st.session_state:
        st.session_state.vector_store = None
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # UI 표시 및 사용자 입력 받기
    uploaded_file, question, selected_models = display_ui()

    # PDF 파일이 업로드되면 RAG 파이프라인 실행
    # st.session_state를 사용하여 이전에 업로드된 파일인지 확인
    if uploaded_file and st.session_state.get("uploaded_file_name") != uploaded_file.name:
        with st.spinner("PDF를 처리 중입니다... 잠시만 기다려주세요."):
            st.session_state.vector_store = build_rag_pipeline(uploaded_file)
            st.session_state.uploaded_file_name = uploaded_file.name # 파일 이름 저장
            st.session_state.messages = [] # 새 파일이 업로드되면 대화 기록 초기화
        st.success("PDF 처리가 완료되었습니다. 이제 질문을 입력해주세요.")

    # 질문이 있고, 모델이 선택되었으며, 벡터 저장소가 준비된 경우
    if question and any(selected_models.values()) and st.session_state.vector_store:
        # 사용자 질문을 메시지에 추가
        st.session_state.messages.append({"role": "user", "content": question})

        # LLM 응답 받아오기
        with st.spinner("LLM 모델들의 답변을 생성 중입니다..."):
            active_models = {name: selected for name, selected in selected_models.items() if selected}
            responses = get_llm_responses(
                question=question,
                vector_store=st.session_state.vector_store,
                selected_models=active_models
            )
        
        # LLM 응답을 메시지에 추가
        st.session_state.messages.append({"role": "assistant", "content": responses})

    # 대화 기록 표시
    if st.session_state.messages:
        for message in st.session_state.messages:
            # role에 따라 아이콘 분기
            avatar = "🧑‍💻" if message["role"] == "user" else "🤖"
            with st.chat_message(message["role"], avatar=avatar):
                if isinstance(message["content"], dict): # LLM 응답인 경우
                     display_results(message["content"])
                else: # 사용자 질문인 경우
                    st.markdown(message["content"])


if __name__ == "__main__":
    main()