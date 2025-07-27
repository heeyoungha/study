# 🚀 Study Project - 통합 모니터링 시스템

이 프로젝트는 Spring Boot, Django, FastAPI로 구성된 마이크로서비스 아키텍처를 기반으로 한 통합 모니터링 시스템입니다.

## 📊 모니터링 시스템 개요

### 🎯 **통합 모니터링 대시보드**
- **URL**: `http://localhost/unified-monitoring`
- **제공 서비스**: Java Spring Boot
- 모든 서비스의 상태를 한눈에 확인
- 실시간 CPU, 메모리 사용률 모니터링
- 에러 로그 실시간 확인
- 자동 새로고침 (30초마다)

### 🔧 **개별 서비스 모니터링**

#### 1. Spring Boot 모니터링
- **URL**: `http://localhost/api/monitoring/sys-health`
- JVM 힙 메모리, 스레드 정보
- CPU 사용률 및 시스템 로드
- 최근 에러 로그 블록

#### 2. Python FastAPI 모니터링
- **URL**: `http://localhost/python/check-health`
- 시스템 리소스 사용량
- 프로세스별 메모리 사용량
- 최근 에러 로그
- 성능 히스토리

#### 3. Django Commerce 모니터링
- **URL**: `http://localhost/commerce/monitoring/sys-health/`
- Django 애플리케이션 상태
- 데이터베이스 연결 상태
- 캐시 상태 확인
- Store 앱 및 Admin 앱 상태
- Django 설정 정보

## 🏗️ 아키텍처

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Spring Boot   │    │  Python FastAPI │    │  Django Commerce│
│   (Port: 8080)  │    │   (Port: 8000)  │    │   (Port: 8002)  │
│  [통합 대시보드] │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   Nginx Proxy   │
                    │   (Port: 80)    │
                    └─────────────────┘
                                 │
                    ┌─────────────────┐
                    │  MySQL Database │
                    │   (Port: 3306)  │
                    └─────────────────┘
```

## 🚀 시작하기

### 1. 환경 설정
```bash
# 프로젝트 클론
git clone <repository-url>
cd study

# 환경 변수 설정
cp .env.example .env
# .env 파일을 편집하여 필요한 환경 변수 설정
```

### 2. Docker Compose로 실행
```bash
# 모든 서비스 시작
docker-compose up -d

# 로그 확인
docker-compose logs -f

# 특정 서비스 로그 확인
docker-compose logs -f app          # Spring Boot
docker-compose logs -f python-api   # FastAPI
docker-compose logs -f django-commerce # Django
```

### 3. 모니터링 접근
- **통합 대시보드**: http://localhost/unified-monitoring
- **Spring Boot**: http://localhost/admin/sys-health
- **FastAPI**: http://localhost/python/admin/sys-health
- **Django**: http://localhost/commerce/admin/sys-health/

## 📈 모니터링 기능

### 🔍 **실시간 모니터링**
- CPU 사용률 (실시간)
- 메모리 사용률 (실시간)
- 시스템 업타임
- 에러 로그 분석

### 📊 **히스토리 추적**
- 최근 30개 데이터 포인트 저장
- 1분마다 자동 업데이트
- 그래프 형태로 시각화

### 🚨 **에러 감지**
- 최근 30분 에러 로그 블록 분석
- 실시간 에러 알림
- 에러 패턴 분석

### 🧪 **테스트 기능**
- 500 에러 테스트 엔드포인트
- 서비스별 개별 테스트
- 통합 테스트 기능

## 🔧 기술 스택

### Backend Services
- **Spring Boot**: Java 기반 메인 애플리케이션 (통합 모니터링 대시보드 제공)
- **FastAPI**: Python 기반 API 서버
- **Django**: Python 기반 웹 애플리케이션

### Infrastructure
- **Docker**: 컨테이너화
- **Nginx**: 리버스 프록시
- **MySQL**: 데이터베이스

### Monitoring
- **Custom Health Checks**: 각 서비스별 커스텀 헬스체크
- **Real-time Metrics**: 실시간 메트릭 수집
- **Error Logging**: 에러 로그 분석
- **Unified Dashboard**: 통합 모니터링 대시보드 (Spring Boot에서 제공)

## 📁 프로젝트 구조

```
study/
├── src/                    # Spring Boot 소스 (통합 모니터링 포함)
├── python-api/            # FastAPI 서비스
├── django-commerce/       # Django 서비스
├── nginx/                # Nginx 설정
├── database/             # MySQL 설정
├── logs/                 # 로그 파일들
└── docker-compose.yml    # Docker Compose 설정
```

## 🛠️ 개발 가이드

### 새로운 서비스 추가
1. 서비스별 모니터링 엔드포인트 구현
2. 통합 대시보드에 서비스 추가 (Spring Boot의 AdminHealthController.java 수정)
3. nginx 설정 업데이트
4. docker-compose.yml에 서비스 추가

### 모니터링 확장
1. 추가 메트릭 수집
2. 알림 시스템 구현
3. 대시보드 커스터마이징
4. 로그 분석 강화

### 📝 API 문서

#### 헬스체크 엔드포인트
- **Spring Boot**: `GET /admin/sys-health`
- **Python FastAPI**: `GET /python/admin/sys-health` (JSON), `GET /python/check-health` (HTML)
- **Django Commerce**: `GET /commerce/monitoring/sys-health/`

#### 테스트 엔드포인트 (500 에러 시뮬레이션)
- **Spring Boot**: `GET /admin/test-500`
- **Python FastAPI**: `GET /python/admin/test-500`
- **Django Commerce**: `GET /commerce/monitoring/test-500/`

### Monitoring Dashboard
- `GET /unified-monitoring`