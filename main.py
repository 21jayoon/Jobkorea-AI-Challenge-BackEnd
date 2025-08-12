import uvicorn
from dotenv import load_dotenv
import uuid
from typing import List, Annotated, Optional
from enum import Enum

from fastapi import FastAPI, Form, HTTPException, Request
from pydantic import BaseModel, Field

from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.messages import BaseMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_core.runnables.history import RunnableWithMessageHistory

load_dotenv()

model = ChatOpenAI(
    model_name='gpt-4o',
    temperature=0.7
)

# 사용자 상태를 관리하기 위한 Enum
class UserState(str, Enum):
    START = "start"
    INPUT_METHOD_SELECTION = "input_method_selection"
    FORM_INPUT = "form_input"
    LONG_TEXT_INPUT = "long_text_input"
    SUMMARY_CONFIRMATION = "summary_confirmation"
    CONCERN_INPUT = "concern_input"
    QUESTIONS_GENERATED = "questions_generated"
    QUESTIONS_CONFIRMATION = "questions_confirmation"
    LEARNING_PATH = "learning_path"

# 세션 데이터 모델
class SessionData(BaseModel):
    state: UserState = UserState.START
    career: Optional[str] = None
    job_duties: Optional[str] = None
    tech_skills: Optional[str] = None
    long_text: Optional[str] = None
    summary: Optional[str] = None
    concern: Optional[str] = None
    questions: List[str] = []
    learning_path: Optional[str] = None

# 전역 저장소
store = {}
session_data_store = {}

def get_by_session_id(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

def get_session_data(session_id: str) -> SessionData:
    if session_id not in session_data_store:
        session_data_store[session_id] = SessionData()
    return session_data_store[session_id]

# 프롬프트 템플릿
system_prompt = """
당신은 IT 분야 취업 준비생을 위한 전문 면접 상담사입니다. 
구직자의 이력서 정보를 바탕으로 실제 면접에서 나올 법한 심층적인 질문을 생성하고, 
개인 맞춤형 자기 개발 학습 경로를 제안하는 것이 목표입니다.

모든 답변은 친근하고 도움이 되는 톤으로 한국어로 작성해주세요.
"""

prompt = ChatPromptTemplate.from_messages([
    ('system', system_prompt),
    MessagesPlaceholder(variable_name='history'),
    ('human', '{query}')
])

chain = prompt | model

chain_with_history = RunnableWithMessageHistory(
    runnable=chain,
    get_session_history=get_by_session_id,
    input_messages_key='query',
    history_messages_key='history'
)

app = FastAPI(title="면접 모의질문 챗봇 API")

@app.post("/help/job-interview", summary="면접 준비 도우미 챗봇")
async def job_interview_helper(
    message: Annotated[str, Form(...)], 
    session_id: Annotated[str, Form(...)],
    career: Annotated[str, Form()] = None,
    job_duties: Annotated[str, Form()] = None,
    tech_skills: Annotated[str, Form()] = None,
    long_text: Annotated[str, Form()] = None
):
    session_data = get_session_data(session_id)
    
    # 상태에 따른 처리
    if session_data.state == UserState.START:
        session_data.state = UserState.INPUT_METHOD_SELECTION
        return {
            "message": "안녕하세요! 면접 준비를 도와드릴게요. 먼저 이력서 정보를 입력해주세요.",
            "buttons": [
                {"text": "폼 입력으로 간단하게 이력서 정보를 넣을래.", "value": "form_input"},
                {"text": "설명을 나열할테니 이력서 핵심 정보로 요약해줘.", "value": "long_text_input"}
            ],
            "state": session_data.state
        }
    
    elif session_data.state == UserState.INPUT_METHOD_SELECTION:
        if message == "form_input":
            session_data.state = UserState.FORM_INPUT
            return {
                "message": "폼을 통해 이력서 정보를 입력해주세요.",
                "form": {
                    "career": {"label": "경력 (예: 3년차 백엔드 개발자)", "maxlength": 100},
                    "job_duties": {"label": "수행 직무 (예: Spring Boot/MSA/Python 기반 커머스 서비스 개발)", "maxlength": 100},
                    "tech_skills": {"label": "보유 기술 스킬 리스트 (예: AWS EC2 운영 경험 있음)", "maxlength": 100}
                },
                "state": session_data.state
            }
        elif message == "long_text_input":
            session_data.state = UserState.LONG_TEXT_INPUT
            return {
                "message": "경력, 수행 업무, 기술 스킬 등에 대해 자유롭게 설명해주세요.",
                "form": {
                    "long_text": {"label": "자유 설명", "type": "textarea", "maxlength": 600}
                },
                "state": session_data.state
            }
    
    elif session_data.state == UserState.FORM_INPUT:
        if career and job_duties and tech_skills:
            session_data.career = career
            session_data.job_duties = job_duties
            session_data.tech_skills = tech_skills
            session_data.state = UserState.CONCERN_INPUT
            
            return {
                "message": f"이력서 정보를 잘 받았습니다!\n경력: {career}\n수행 직무: {job_duties}\n보유 기술: {tech_skills}\n\n이력서 정보 중 면접에서 어떤 부분과 관련한 질문이 나올까봐 제일 걱정되시나요?",
                "state": session_data.state
            }
        else:
            return {
                "message": "모든 필드를 입력해주세요.",
                "error": True
            }
    
    elif session_data.state == UserState.LONG_TEXT_INPUT:
        if long_text:
            session_data.long_text = long_text
            
            # AI를 사용하여 요약 생성
            summary_query = f"""
            다음 긴 설명을 이력서 핵심 정보로 요약해주세요:
            "{long_text}"
            
            다음 형식으로 요약해주세요:
            "X년차 [직무]개발자(경력), [구체적인 업무 내용](수행 직무), [기술 스택들] 사용 가능(보유 기술 스킬 리스트)"
            
            요약 후에는 "이렇게 이력서 핵심 내용을 정리했어. 이게 맞아?"라고 물어보세요.
            """
            
            response = chain_with_history.invoke(
                {'query': summary_query},
                config={'configurable': {'session_id': session_id}}
            )
            
            session_data.summary = response.content
            session_data.state = UserState.SUMMARY_CONFIRMATION
            
            return {
                "message": response.content,
                "buttons": [
                    {"text": "맞아", "value": "confirm_yes"},
                    {"text": "틀렸어", "value": "confirm_no"},
                    {"text": "추가하고 싶은 부분이 있어", "value": "confirm_no"}
                ],
                "state": session_data.state
            }
        else:
            return {
                "message": "설명을 입력해주세요.",
                "error": True
            }

    elif session_data.state == UserState.SUMMARY_CONFIRMATION:
        if message == "confirm_yes" or "맞" in message or "좋" in message or "잘" in message:
            session_data.state = UserState.CONCERN_INPUT
            return {
                "message": "이력서 정보 중 면접에서 어떤 부분과 관련한 질문이 나올까봐 제일 걱정되시나요?",
                "state": session_data.state
            }
        else:
            # 다시 긴 글 입력으로
            session_data.state = UserState.LONG_TEXT_INPUT
            return {
                "message": "다시 설명해주세요. 이전 내용을 수정하거나 추가해서 작성하실 수 있습니다.",
                "form": {
                    "long_text": {"label": "자유 설명", "type": "textarea", "maxlength": 600, "value": session_data.long_text}
                },
                "state": session_data.state
            }
    
    elif session_data.state == UserState.CONCERN_INPUT:
        session_data.concern = message
        session_data.state = UserState.QUESTIONS_GENERATED
        
        # 이력서 정보 준비
        if session_data.career:
            resume_info = f"경력: {session_data.career}, 수행 직무: {session_data.job_duties}, 보유 기술: {session_data.tech_skills}"
        else:
            resume_info = session_data.summary
        
        # AI를 사용하여 면접 질문 생성
        questions_query = f"""
        다음 이력서 정보를 바탕으로 실제 면접에서 나올 법한 심층적인 질문 5개를 생성해주세요:
        {resume_info}
        
        사용자의 걱정: {session_data.concern}
        
        각 질문 뒤에는 괄호 안에 해당 질문이 경력, 수행 직무, 보유 기술 스킬 중 어떤 것과 연관되어 있는지 명시해주세요.
        
        예시: "Spring Boot/Java를 기반으로 학부 시간표 개발했다고 하셨는데, 스프링 Bean의 Scope에 대해 설명해주세요.(수행 직무)"
        
        5번째 질문 후에는 반드시 다음 문구를 추가해주세요:
        "질문에 관해 음성메모로 답을 해본 후 답변한 내용이 잘 전달되는 것 같은지, 답변 내용에 아쉬운 점은 없는지 확인해보세요."
        """
        
        response = chain_with_history.invoke(
            {'query': questions_query},
            config={'configurable': {'session_id': session_id}}
        )
        
        return {
            "message": response.content + "\n\n질문 5개가 마음에 드셨나요?",
            "buttons": [
                {"text": "예", "value": "questions_yes"},
                {"text": "아니오", "value": "questions_no"}
            ],
            "state": session_data.state
        }
    
    elif session_data.state == UserState.QUESTIONS_GENERATED:
        if message == "questions_yes":
            session_data.state = UserState.LEARNING_PATH
            
            # 이력서 정보 준비
            if session_data.career:
                resume_info = f"경력: {session_data.career}, 수행 직무: {session_data.job_duties}, 보유 기술: {session_data.tech_skills}"
            else:
                resume_info = session_data.summary
            
            # AI를 사용하여 학습 경로 생성
            learning_query = f"""
            다음 이력서 정보를 분석하여 개인 맞춤형 자기 개발 및 합격률 향상 학습 경로를 제안해주세요:
            {resume_info}
            
            사용자의 걱정: {session_data.concern}
            
            다음과 같은 구체적인 방안들을 포함해주세요:
            - 특정 기술 스택 심화 학습
            - 관련 프로젝트 경험 쌓기  
            - 커뮤니케이션 스킬 강화
            - 기타 면접 합격률을 높일 수 있는 구체적인 방법들
            
            예시 형태로 자세하고 실용적인 조언을 제공해주세요.
            """
            
            response = chain_with_history.invoke(
                {'query': learning_query},
                config={'configurable': {'session_id': session_id}}
            )
            
            return {
                "message": "🎯 **개인 맞춤 학습 경로 추천**\n\n" + response.content,
                "state": session_data.state,
                "final": True
            }
            
        elif message == "questions_no":
            # 다른 질문 5개 생성
            if session_data.career:
                resume_info = f"경력: {session_data.career}, 수행 직무: {session_data.job_duties}, 보유 기술: {session_data.tech_skills}"
            else:
                resume_info = session_data.summary
            
            questions_query = f"""
            다음 이력서 정보를 바탕으로 이전과는 다른 새로운 실제 면접에서 나올 법한 심층적인 질문 5개를 생성해주세요:
            {resume_info}
            
            각 질문 뒤에는 괄호 안에 해당 질문이 경력, 수행 직무, 보유 기술 스킬 중 어떤 것과 연관되어 있는지 명시해주세요.
            
            5번째 질문 후에는 반드시 다음 문구를 추가해주세요:
            "질문에 관해 음성메모로 답을 해본 후 답변한 내용이 잘 전달되는 것 같은지, 답변 내용에 아쉬운 점은 없는지 확인해보세요."
            """
            
            response = chain_with_history.invoke(
                {'query': questions_query},
                config={'configurable': {'session_id': session_id}}
            )
            
            return {
                "message": response.content + "\n\n질문 5개가 마음에 드셨나요?",
                "buttons": [
                    {"text": "예", "value": "questions_yes"},
                    {"text": "아니오", "value": "questions_no"}
                ],
                "state": session_data.state
            }
    
    return {
        "message": "죄송합니다. 처리할 수 없는 요청입니다.",
        "error": True
    }

@app.post("/init_conversation")
async def init_conversation():
    session_id = str(uuid.uuid4())
    get_by_session_id(session_id)  # session ID 생성
    get_session_data(session_id)   # session data 생성
    return {"session_id": session_id}

@app.delete("/remove_conversation")
async def remove_conversation(session_id: Annotated[str, Form(...)]):
    if session_id in store:
        store.pop(session_id)
    if session_id in session_data_store:
        session_data_store.pop(session_id)
    else:
        raise HTTPException(status_code=404, detail="session_id not found")
    return {"message": "Conversation removed successfully"}

@app.get("/session_status/{session_id}")
async def get_session_status(session_id: str):
    if session_id not in session_data_store:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session_data = session_data_store[session_id]
    return {
        "session_id": session_id,
        "state": session_data.state,
        "has_resume_info": bool(session_data.career or session_data.summary)
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
