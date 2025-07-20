# 비동기 FastAPI 서비스

이 프로젝트는 FastAPI의 비동기 기능을 활용하여 고성능 API를 제공합니다.

## 주요 변경사항

### 1. 비동기 데이터베이스 연결
- `aiomysql` 드라이버 사용
- `AsyncSession`을 통한 비동기 데이터베이스 작업
- `await` 키워드를 사용한 비동기 쿼리 실행

### 2. 비동기 라우터 함수
- 모든 라우터 함수가 `async def`로 변경
- 데이터베이스 작업에 `await` 사용
- 비동기 템플릿 렌더링

### 3. 비동기 서비스 함수
- `save_diary_async()`, `get_all_diaries_async()` 등
- 비동기 데이터베이스 세션 사용
- `await db.commit()`, `await db.refresh()` 사용

## 실행 방법

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. 비동기 서버 실행
```bash
python run_async_server.py
```

### 3. Docker 실행
```bash
docker build -t fastapi-async .
docker run -p 8000:8000 fastapi-async
```

## API 엔드포인트

### Swagger UI
- `/docs` - Swagger UI
- `/redoc` - ReDoc 문서
- `/openapi.json` - OpenAPI 스키마

### 자동 리다이렉트
- `/` → `/docs`
- `/swagger` → `/docs`
- `/api-docs` → `/docs`

### 일기 관련
- `GET /diary` - 일기 작성 폼
- `POST /diary` - 일기 저장
- `GET /diary/list` - 일기 목록
- `GET /diary/{diary_id}` - 일기 상세

### 독서모임 관련
- `GET /bookclub` - 독후감 작성 폼
- `POST /bookclub/form` - 독후감 저장 (폼)
- `POST /bookclub/` - 독후감 저장 (JSON API)
- `GET /bookclub/list` - 독후감 목록
- `GET /bookclub/{entry_id}` - 독후감 상세

## 성능 향상

### 1. 동시성 처리
- 여러 요청을 동시에 처리 가능
- I/O 대기 시간 동안 다른 작업 수행

### 2. 데이터베이스 연결 풀
- 비동기 연결 풀로 효율적인 DB 연결 관리
- 연결 재사용으로 성능 향상

### 3. 비동기 템플릿 렌더링
- Jinja2 템플릿 렌더링도 비동기로 처리

## 마이그레이션

기존 동기 코드에서 비동기로 마이그레이션할 때:

1. 함수를 `async def`로 변경
2. 데이터베이스 작업에 `await` 추가
3. `Session`을 `AsyncSession`으로 변경
4. `db.query()`를 `db.execute(select())`로 변경

## 주의사항

1. **비동기 함수 내에서 동기 함수 호출 금지**
2. **데이터베이스 세션은 반드시 `await`로 처리**
3. **외부 API 호출도 비동기로 처리 권장**
4. **에러 처리는 `try/except` 블록에서 `await` 사용** 