# 면접 모의질문 챗봇 API

구직자의 경력과 희망 직무, 기술 스킬 등의 이력서 내용을 기반으로 맞춤 면접 모의질문을 생성하고 자기 개발 학습 경로를 제안해 구직자의 합격률을 높이는 데 도움을 주는 챗봇입니다.

## 🔧 핵심 기능

### 1. 상태 관리 시스템
- `UserState` Enum을 통해 사용자의 현재 진행 상태를 추적
- 각 세션별로 독립적인 상태와 데이터 관리

### 2. 이력서 정보 입력 방식
- **폼 입력**: 경력, 수행 직무, 기술 스킬을 각각 100자 이하로 간단 입력
- **긴 글 나열**: 600자 텍스트로 자유롭게 작성 후 AI가 자동 요약

### 3. AI 기반 처리
- **요약 기능**: 긴 글을 구조화된 이력서 정보로 자동 요약
- **질문 생성**: 개인 맞춤형 면접 질문 5개 생성 (각 질문의 연관 분야 표시)
- **학습 경로 추천**: 개인별 맞춤 자기개발 방안 제시

### 4. 사용자 상호작용
- 버튼 기반 선택지 제공
- 요약 내용 확인 및 재작성 기능
- 질문 만족도 확인 후 재생성 옵션

## 📋 API 엔드포인트

### `POST /help/job-interview`
- 메인 챗봇 상호작용 엔드포인트
- 상태별 다른 응답과 처리 로직

### `POST /init_conversation`
- 새 세션 시작 (UUID 기반 세션 ID 생성)

### `DELETE /remove_conversation`
- 세션 데이터 삭제

### `GET /session_status/{session_id}`
- 현재 세션 상태 확인

## 🛠️ 기술 스택

- **Backend**: FastAPI
- **AI Model**: OpenAI GPT-4o
- **Framework**: LangChain
- **Python Version**: 3.8+

## 🚀 실행 방법

### 1. 저장소 클론
```bash
git clone <repository-url>
cd job-interview-chatbot
```

### 2. 필요한 패키지 설치
```bash
pip install -r requirements.txt
```

### 3. 환경 변수 설정
`.env` 파일을 생성하고 OpenAI API 키를 설정하세요:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

### 4. 서버 실행
```bash
python main.py
```

서버가 성공적으로 실행되면 `http://127.0.0.1:8000/docs` 에서 접근할 수 있습니다.

## 💡 사용 흐름

1. **세션 시작** → 입력 방식 선택
2. **이력서 정보 입력** (폼 또는 긴 글)
3. **긴 글의 경우 요약 확인**
4. **걱정되는 부분 입력**
5. **맞춤 면접 질문 5개 생성**
6. **질문 만족도 확인**
7. **개인 맞춤 학습 경로 추천**

## 📁 프로젝트 구조

```
job-interview-chatbot/
├── main.py              # 메인 애플리케이션 파일
├── requirements.txt     # Python 의존성 패키지
├── .env                # 환경 변수 설정
└── README.md           # 프로젝트 문서
```

## 🔍 API 사용 예시

### 세션 시작
```bash
curl -X POST "http://localhost:8000/init_conversation"
```

### 챗봇과 상호작용
```bash
curl -X POST "http://localhost:8000/help/job-interview" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "message=시작&session_id=your-session-id"
```

### 세션 상태 확인
```bash
curl -X GET "http://localhost:8000/session_status/your-session-id"
```

## 📝 응답 형태

챗봇의 응답은 다음과 같은 JSON 형태로 제공됩니다:

```json
{
  "message": "응답 메시지",
  "buttons": [
    {"text": "선택지 1", "value": "option1"},
    {"text": "선택지 2", "value": "option2"}
  ],
  "form": {
    "field_name": {
      "label": "입력 필드 라벨",
      "maxlength": 100,
      "type": "text"
    }
  },
  "state": "current_state",
  "final": false
}
```

## 🆘 문의사항
프로젝트 관련 문의사항이나 버그 리포트는 21jayoon@gmail.com을 통해 제출해주세요.
