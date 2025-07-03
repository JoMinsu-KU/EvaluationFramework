# modules/llm.py
import time
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_anthropic import ChatAnthropic

def get_llm_responses(question, vector_store, selected_models):
    """
    선택된 LLM 모델들로부터 질문에 대한 응답을 받아옵니다.
    """
    responses = {}
    retriever = vector_store.as_retriever()

    template = """
    당신은 주어진 컨텍스트를 바탕으로 질문에 답변하는 AI 어시스턴트입니다.
    컨텍스트를 벗어난 내용은 답변하지 마세요.
    
    컨텍스트: {context}
    
    질문: {question}
    
    답변:
    """
    prompt = ChatPromptTemplate.from_template(template)

    # 모델 초기화
    # API 키는 환경변수에서 자동으로 로드됩니다.
    models = {
        "Gemini 2.5 Pro": ChatGoogleGenerativeAI(model="gemini-2.5-pro-preview-06-05", temperature=0),
        "GPT-4o": ChatOpenAI(model="gpt-4o", temperature=0),
        "Claude 4 Opus": ChatAnthropic(model="claude-opus-4-20250514", temperature=0),
    }

    for model_name, is_selected in selected_models.items():
        if is_selected:
            try:
                start_time = time.time()
                
                llm = models[model_name]
                
                rag_chain = (
                    {"context": retriever, "question": RunnablePassthrough()}
                    | prompt
                    | llm
                    | StrOutputParser()
                )
                
                answer = rag_chain.invoke(question)
                # get_relevant_documents는 LangChain 0.2.0에서 deprecated 될 예정이므로, retriever.invoke를 사용합니다.
                source_documents = retriever.invoke(question)
                
                end_time = time.time()
                
                responses[model_name] = {
                    "answer": answer,
                    "response_time": end_time - start_time,
                    "source_documents": source_documents
                }
            except Exception as e:
                responses[model_name] = {
                    "answer": f"**오류 발생:** {e}",
                    "response_time": 0,
                    "source_documents": []
                }
            
    return responses