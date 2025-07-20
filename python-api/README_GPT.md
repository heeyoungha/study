# GPT 기반 감정 분석 및 프로젝트 추천 시스템

이 프로젝트는 OpenAI GPT API를 활용하여 일기 텍스트의 감정을 분석하고, 감정에 맞는 프로젝트를 추천하는 시스템입니다.

## 🚀 주요 기능

### 1. GPT 기반 감정 분석
- **정확한 감정 분류**: positive, negative, neutral
- **신뢰도 점수**: 분석 결과의 신뢰도 제공
- **분석 이유**: 왜 그런 감정으로 분류했는지 설명

### 2. GPT 기반 프로젝트 추천
- **맞춤형 추천**: 감정과 내용을 바탕으로 한 개인화된 추천
- **다양한 카테고리**: 자기계발, 사회활동, 건강관리, 창작활동, 기술활동
- **추천 이유**: 왜 그 프로젝트를 추천하는지 설명

### 3. Fallback 시스템
- **API 실패 시**: 기본 키워드 기반 분석으로 대체
- **안정성 보장**: GPT API 오류 시에도 서비스 중단 없음

## 🔧 설정 방법

### 1. 환경변수 설정
`.env` 파일에 다음 내용을 추가하세요:

```env
# OpenAI API 설정
OPENAI_API_KEY=your_openai_api_key_here

# 데이터베이스 설정
DATASOURCE_USERNAME=your_db_username
DATASOURCE_PASSWORD=your_db_password
DATASOURCE_HOST=localhost
DATASOURCE_PORT=3306
DATASOURCE_DB=your_database_name
```

### 2. 의존성 설치
```bash
pip install -r requirements.txt
```

### 3. 서버 실행
```bash
python run_async_server.py
```

## 📡 API 엔드포인트

### 서비스 상태 확인
```http
GET /python/health
```

**응답 예시:**
```json
{
    "status": "healthy",
    "services": {
        "gpt_api": "available",
        "analysis_quality": "enhanced"
    },
    "warnings": []
}
```

### 관리자 대시보드
```http
GET /python/admin/dashboard
```

**응답 예시:**
```json
{
    "dashboard": {
        "service_quality": "excellent",
        "quality_score": 95
    },
    "alerts": []
}
```

### 감정 분석 API
```http
POST /diary/sentiment-analysis
Content-Type: application/json

{
    "text": "오늘은 정말 기쁜 하루였다. 새로운 프로젝트를 시작하게 되어 설렌다."
}
```

**응답 예시:**
```json
{
    "text": "오늘은 정말 기쁜 하루였다. 새로운 프로젝트를 시작하게 되어 설렌다.",
    "sentiment": "positive",
    "confidence": 0.95,
    "reason": "텍스트에서 '기쁜', '설렌다' 등의 긍정적 감정 표현이 나타남",
    "analysis_method": "GPT API 사용"
}
```

### 프로젝트 추천 API
```http
POST /diary/project-recommendation
Content-Type: application/json

{
    "text": "오늘은 정말 기쁜 하루였다. 새로운 프로젝트를 시작하게 되어 설렌다.",
    "sentiment": "positive"
}
```

**응답 예시:**
```json
{
    "text": "오늘은 정말 기쁜 하루였다. 새로운 프로젝트를 시작하게 되어 설렌다.",
    "sentiment": "positive",
    "projects": [
        "리더십 개발 프로그램",
        "창의적 프로젝트 관리",
        "멘토링 활동"
    ],
    "reason": "긍정적인 에너지와 새로운 시작에 대한 설렘을 바탕으로 성장 지향적 활동 추천",
    "recommendation_method": "GPT API 사용"
}
```

## 🎯 사용 예시

### 1. 일기 작성 시 자동 감정 분석
```python
# 일기 제출 시 자동으로 GPT 감정 분석 수행
POST /diary
Form Data:
- summary: "새로운 프로젝트 시작"
- content: "오늘은 정말 기쁜 하루였다..."
```

### 2. 독후감 작성 시 프로젝트 추천
```python
# 독후감 제출 시 GPT 기반 프로젝트 추천
POST /bookclub/form
Form Data:
- book_title: "자기계발의 기술"
- review: "이 책을 읽고 많은 영감을 받았다..."
- summary: "성장에 대한 새로운 관점"
```

## 🔍 GPT 프롬프트 구조

### 감정 분석 프롬프트
```
다음 일기 텍스트의 감정을 분석하여 다음 중 하나로 분류해주세요:
- positive (긍정적): 기쁨, 행복, 만족, 감사, 희망, 설렘, 성취감 등
- negative (부정적): 슬픔, 우울, 분노, 불안, 스트레스, 실망, 외로움 등  
- neutral (중립적): 평온, 일상, 객관적, 무관심 등

응답은 반드시 다음 JSON 형식으로만 해주세요:
{"sentiment": "positive|negative|neutral", "confidence": 0.95, "reason": "분석 이유"}
```

### 프로젝트 추천 프롬프트
```
다음 일기 내용을 바탕으로 사용자에게 도움이 될 만한 프로젝트나 활동을 추천해주세요.

다음 카테고리 중에서 추천해주세요:
- 자기계발: 학습, 스킬 개발, 취미 활동
- 사회활동: 봉사, 모임, 네트워킹
- 건강관리: 운동, 명상, 휴식
- 창작활동: 글쓰기, 예술, 공예
- 기술활동: 프로그래밍, 디자인, 개발

응답은 반드시 다음 JSON 형식으로만 해주세요:
{"projects": ["프로젝트1", "프로젝트2", "프로젝트3"], "reason": "추천 이유"}
```

## 🛡️ 오류 처리

### 1. GPT API 오류 시
- **Fallback 시스템**: 기본 키워드 기반 분석으로 대체
- **안정성 보장**: 서비스 중단 없이 계속 운영

### 2. JSON 파싱 오류 시
- **텍스트 기반 추출**: 응답에서 감정 키워드 추출
- **기본값 사용**: 안전한 기본값으로 처리

## 📊 성능 최적화

### 1. 비동기 처리
- **동시 요청 처리**: 여러 감정 분석 요청을 동시에 처리
- **응답 시간 단축**: 비동기 API 호출로 성능 향상

### 2. 캐싱 (향후 구현 예정)
- **결과 캐싱**: 동일한 텍스트에 대한 중복 분석 방지
- **Redis 연동**: 빠른 캐시 조회

## 🔮 향후 개선 계획

1. **감정 세분화**: 더 세밀한 감정 분류 (기쁨, 슬픔, 분노, 불안 등)
2. **맥락 분석**: 문맥을 고려한 더 정확한 감정 분석
3. **개인화**: 사용자별 감정 패턴 학습
4. **실시간 분석**: 실시간 감정 변화 추적
5. **멀티모달**: 텍스트 외 이미지, 음성 등 다양한 입력 지원

## 💡 사용 팁

1. **API 키 보안**: `.env` 파일을 `.gitignore`에 추가하여 API 키 보호
2. **비용 관리**: GPT API 사용량 모니터링
3. **오류 로깅**: GPT API 오류 시 로그 확인
4. **성능 모니터링**: 응답 시간 및 정확도 추적

## 🌐 접속 URL

### 개발자 도구
- **Swagger UI**: `http://localhost:8000/python/docs`
- **ReDoc**: `http://localhost:8000/python/redoc`
- **OpenAPI JSON**: `http://localhost:8000/python/openapi.json`

### 서비스 상태 확인
- **헬스체크**: `http://localhost:8000/python/health`
- **관리자 대시보드**: `http://localhost:8000/python/admin/dashboard`

### 사용자 페이지
- **일기 작성**: `http://localhost:8000/diary`
- **일기 목록**: `http://localhost:8000/diary/list`
- **독서모임**: `http://localhost:8000/bookclub` 