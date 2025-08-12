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
```cmd
git clone https://github.com/21jayoon/Jobkorea-AI-Challenge-BackEnd.git
cd job-interview-chatbot
```
(개발은 VS code로 이루어졌습니다. 
VS code 사용을 권장합니다.)

### 2. 필요한 패키지 설치
```cmd
pip install -r requirements.txt
```
위 명령어로 한 번에 설치 불가할 시,

```cmd
pip install [각 패키지 이름]
```
로 하나씩 설치 필요
예시) pip install uvicorn
pip install langchain_openai

### 3. 환경 변수 설정
`.env` 파일을 생성하고 OpenAI API 키를 설정하세요:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

챗지피티 개발사인 OPENAI의 API 키를 사용하였습니다.
이 GitHub 파일을 pull 혹은 clone한 후 
귀사가 지원하는 혹은 연동 가능한 API 키를 env 파일 안에 넣고
테스트하시면 됩니다.
만일 OPENAPI사가 아닌 다른 곳(예.Anthropic-claude개발사)을 사용한다면
main.py에 있는  from langchain_openai import ChatOpenAI  대신
from langchain_anthropic import ChatAnthropic
등을 사용해야합니다.


### 4. 서버 실행
```cmd
python main.py
```

* Swagger 사용 시 
```cmd
uvicorn main:app --reload
```
혹은 
```cmd
python -m uvicorn main:app --reload
```
사용 요망

서버가 성공적으로 실행되면 `http://127.0.0.1:8000` 에서 접근할 수 있습니다.
(fastAPI를 사용해서 Swagger에도 접근 가능하기 때문에 http://127.0.0.1:8000/docs 로의 접근을 더 추천합니다.)

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
## ⭐ Swagger를 통한 확인
requirements.txt를 이용해 필요한 패키지를 전부 설치한 후 
http://127.0.0.1:8000/docs 에 접속해 기능을 확인합니다.
<img width="1433" height="614" alt="스크린샷 2025-08-12 112754" src="https://github.com/user-attachments/assets/d7bf9915-9dc0-4504-82b5-c6a673b37d13" />


첫 번째로 /init_conversation 에서 'Try it out', 'Execute'버튼을 눌러
아래 server_response에서 session_id를 복사합니다.
<img width="504" height="297" alt="image" src="https://github.com/user-attachments/assets/5cdad72f-6c6d-4405-8e74-70fdf1f3daa6" />

위로 올라가서 /help/job-interview 의 'Try it out'을 누릅니다.
<img width="1506" height="944" alt="image" src="https://github.com/user-attachments/assets/566cebc7-624a-4802-a852-5f2abe16ecde" />

아래에서 복사해온 session_id를 session_id 창에다 넣습니다.
<img width="1420" height="547" alt="image" src="https://github.com/user-attachments/assets/ed459e2a-560c-48ba-ba27-3dc26bdc8345" />

Execute를 누르고 Response 결과를 확인합니다.
<img width="974" height="683" alt="image" src="https://github.com/user-attachments/assets/7b63b312-22d6-4765-bcbb-73d413c52b33" />

### form_input (단문, 명사 위주 입력) 사용
1. message 부분에 form_input을 넣고
Execute를 눌러 결과를 확인합니다.
<img width="564" height="148" alt="image" src="https://github.com/user-attachments/assets/eba6b0fb-104c-4658-b749-6c8454ff33d4" />

2. 이후 관련 폼에 경력, 수행 직무, 보유 기술 스킬 리스트를 작성합니다.
<img width="569" height="602" alt="image" src="https://github.com/user-attachments/assets/74f049eb-7a4a-49cd-8924-d7ac71d660cb" />

Execute를 누르고 결과를 확인합니다.
<img width="1393" height="370" alt="image" src="https://github.com/user-attachments/assets/f91cc77b-ec50-4eaa-9a93-24a6647f8eda" />

3. 질문에 따라 면접 시 걱정되는 부분을 작성하고
<img width="539" height="64" alt="image" src="https://github.com/user-attachments/assets/ede5665f-3a80-4916-870c-f65829cbe2b6" />
Execute를 눌러 결과를 확인합니다.
<img width="1309" height="290" alt="image" src="https://github.com/user-attachments/assets/9f3bb770-489c-4b4d-a883-ab498fa62581" />

다른 면접질문 다섯 개를 다시 받기 위해 message 폼에 questions_no를 입력합니다.
<img width="533" height="59" alt="image" src="https://github.com/user-attachments/assets/17bd14c4-4a53-4fbf-a0ad-de698f08e880" />

4. 새 질문 5개를 확인 후 questions_yes를 입력해 다음인 학습 경로 추천 단계로 넘어갑니다.
<img width="1308" height="281" alt="image" src="https://github.com/user-attachments/assets/3b925f78-3aff-4c0f-8da2-4888a0599457" />

<img width="523" height="54" alt="image" src="https://github.com/user-attachments/assets/dd09ccc9-4b04-4628-b955-5ea0c521e489" />

개인 맞춤 학습 경로 추천을 받았습니다.
<img width="1308" height="243" alt="image" src="https://github.com/user-attachments/assets/03d2d67a-60a7-4619-8598-56ca4029991a" />

### long_text_input 사용
1. 새로운 session_id를 받고 long_text_input을 통해 맞춤형 면접 모의 질문을 생성합니다.
<img width="552" height="710" alt="image" src="https://github.com/user-attachments/assets/5879b1a6-85e5-4faa-959d-8f625e1b5b3a" />

<img width="611" height="246" alt="image" src="https://github.com/user-attachments/assets/c1b983cf-63be-4d4b-83f6-062f0d7f81bb" />

이번에는 long_text_input을 통해 긴 이력서 내용을 넣어보고 요약한 내용을 토대로 면접 모의 질문 생성을 시도합니다.
<img width="541" height="229" alt="image" src="https://github.com/user-attachments/assets/d822c7c0-53d7-4b25-89c7-f7147ea7397a" />

<img width="620" height="357" alt="image" src="https://github.com/user-attachments/assets/a2946af5-0979-4ad1-9fe9-970aaed04918" />

2. 이력서에 쓰일 만한 내용을 긴 글로 작성해서 넣고 Execute 버튼을 누릅니다.
   <img width="695" height="239" alt="image" src="https://github.com/user-attachments/assets/a0624404-4791-4d5f-88ec-d3be01497d24" />

3. 요약된 정보를 확인하고 다음 단계로 넘어갈지, 다시 요약을 시도할지, 추가 사항을 넣을지 선택한다.
   <img width="1307" height="313" alt="image" src="https://github.com/user-attachments/assets/c45d044f-54ea-44b8-88de-52eeb0e7cc53" />

   이전 내용을 기억하는지 확인하기 위해 confirm_no를 long_text_input 내용을 지운 채로 실행해보았다.
   <img width="691" height="639" alt="image" src="https://github.com/user-attachments/assets/43bbf68d-c113-4325-8f06-50de084e12d4" />

  잘 기억하고 있는 걸 확인할 수 있다.
   <img width="1301" height="226" alt="image" src="https://github.com/user-attachments/assets/9889dc0c-248b-4591-803c-441943088106" />

4. 기억한 내용을 복사, 거기에 추가 사항을 덧붙여 다시 한 번 실행해보았다.
<img width="686" height="213" alt="image" src="https://github.com/user-attachments/assets/d0b6e6a1-2f16-4b37-aac8-a24bbc837b0f" />

<img width="1294" height="314" alt="image" src="https://github.com/user-attachments/assets/744ee520-be7f-4636-835c-a845cc9fbe21" />

5. message에 confirm_yes를 넣어 면접 걱정되는 부분에 관한 사항에 답했다.
<img width="629" height="97" alt="image" src="https://github.com/user-attachments/assets/6a2e5bfd-062a-4bf4-a5a1-97c90403162b" />

<img width="509" height="60" alt="image" src="https://github.com/user-attachments/assets/a031a861-5d87-4495-8ed8-45b9eef5817c" />

6. 맞춤형 면접질문을 확인했다.
  <img width="1306" height="305" alt="image" src="https://github.com/user-attachments/assets/cc58b7e3-747b-40a2-9807-e55bfb700265" />
 
7. questions_yes라고 답하고 개인 맞춤형 학습 경로 추천을 받는다.
   <img width="1299" height="248" alt="image" src="https://github.com/user-attachments/assets/19174259-dafb-4a78-8bdd-eff2e0140bb6" />


### 세션 시작
```cmd
curl -X POST "http://localhost:8000/init_conversation"
```

### 챗봇과 상호작용
```cmd
curl -X POST "http://localhost:8000/help/job-interview" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "message=시작&session_id=your-session-id"
```

### 세션 상태 확인
```cmd
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
