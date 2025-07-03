# modules/ui.py
import streamlit as st

def display_ui():
    """
    Streamlit UI 컴포넌트를 표시하고 사용자 입력을 반환합니다.
    """
    st.set_page_config(page_title="RAG 기반 LLM 비교 평가 도구", layout="wide")
    st.title("RAG 기반 LLM 비교 평가 도구")
    st.markdown("""
    PDF 파일을 업로드하고 질문을 입력하면, 선택한 LLM 모델들의 답변을 비교하여 확인할 수 있습니다.
    """)

    with st.sidebar:
        st.header("1. 파일 업로드")
        uploaded_file = st.file_uploader("비교할 PDF 파일을 업로드하세요.", type="pdf")

        st.header("2. 모델 선택")
        selected_models = {
            "Gemini 2.5 Pro": st.checkbox("Gemini 2.5 Pro", value=True),
            "GPT-4o": st.checkbox("GPT-4o", value=True),
            "Claude 4 Opus": st.checkbox("Claude 4Opus", value=True),
        }

    question = st.chat_input("PDF 내용에 대해 질문을 입력하세요.")

    return uploaded_file, question, selected_models

def display_results(responses):
    """
    LLM 응답 결과를 컬럼 형태로 표시합니다.
    """
    # 응답이 있는 모델의 수만큼 컬럼 생성
    valid_responses = {k: v for k, v in responses.items() if v}
    if not valid_responses:
        st.warning("표시할 응답이 없습니다.")
        return

    cols = st.columns(len(valid_responses))
    for i, (model_name, result) in enumerate(valid_responses.items()):
        with cols[i]:
            st.subheader(f"🤖 {model_name}")
            st.info(f"응답 시간: {result['response_time']:.2f}초")
            st.markdown(result["answer"])
            with st.expander("참고한 컨텍스트 보기"):
                for doc in result["source_documents"]:
                    st.markdown(f"**페이지 {doc.metadata.get('page', 'N/A')}:**")
                    st.caption(doc.page_content)