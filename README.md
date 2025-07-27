# 📌 Let'Sadam 소개
- 주니어 개발자로서의 역량을 키우기 위해 설계한 로드맵을 구현해나가는 개인 프로젝트입니다.
- url : https://letsadam.shop

## 📈 프로젝트 목표
- 체계적인 로드맵 구현을 통해 주니어 개발자로서의 역량 강화
- 클라우드 환경에서 배포 및 운영 경험 축적
- 최신 기술 도구와 프레임워크를 활용하여 실무에 가까운 프로젝트 구축
- 마이크로서비스 아키텍처 경험 축적

## 🛠 개발환경

### 개발 도구
- IntelliJ IDEA
- VS Code
- Docker Desktop

### 백엔드 기술 스택
- **Java**: Spring Boot, Spring Security, Spring Data JPA
- **Python**: FastAPI (비동기 API 서버)
- **Django**: Django Commerce (전자상거래 기능)

### 프론트엔드 기술 스택
- **HTML/CSS/JavaScript**: Bootstrap, jQuery
- **Thymeleaf**: 서버사이드 템플릿 엔진

### 데이터베이스
- **MySQL**: 메인 데이터베이스 (AWS RDS 사용)
- **PostgreSQL**: Python API 서버용 데이터베이스

### 인프라 및 배포
- **Docker**: 다중 컨테이너 구성
- **Docker Compose**: 개발/운영 환경 분리
- **Nginx**: 리버스 프록시 및 정적 파일 서빙
- **AWS**: EC2, RDS, Route 53, VPC

## 🔍 핵심 기능

### 🔐 인증 및 보안
- **OAuth2 소셜 로그인**: Google 로그인 지원
- **JWT 토큰 기반 인증**: API 보안
- **Spring Security**: 웹 애플리케이션 보안

### 📝 게시판 시스템
- **CRUD 기능**: 게시글 작성, 수정, 삭제, 조회
- **검색 기능**: 제목, 내용 기반 검색
- **페이지네이션**: 효율적인 데이터 로딩
- **댓글 시스템**: 게시글별 댓글 기능

### 🗺️ 프로젝트 관리
- **프로젝트 CRUD**: 프로젝트 생성, 수정, 삭제, 조회
- **프로젝트 검색**: 제목, 설명 기반 검색
- **프로젝트 상세 정보**: 프로젝트별 상세 페이지

### ☕ 카페 추천 시스템
- **카카오 API 연동**: 주소 검색 및 좌표 변환
- **주변 카페 검색**: 사용자 위치 기반 카페 추천
- **카페 상세 정보**: 카페 정보 및 위치 표시

### 🛒 전자상거래 (Django Commerce)
- **상품 관리**: 상품 등록, 수정, 삭제
- **장바구니**: 상품 담기 및 주문(예정)
- **결제 시스템**: 결제 프로세스 구현(예정)

### 📊 일기 및 독서모임 (Python API)
- **일기 작성**: 개인 일기 작성 및 관리
- **감정 분석**: GPT를 활용한 감정 분석
- **독서모임**: 독서 기록 및 관리
- **프로젝트 추천**: AI 기반 프로젝트 추천

## 🏗️ 아키텍처

### 마이크로서비스 구성
```
├── Java Spring Boot (메인 애플리케이션)
├── Python FastAPI (일기/독서모임 API)
├── Django Commerce (전자상거래)
├── MySQL (메인 DB)
├── PostgreSQL (Python API DB)
└── Nginx (리버스 프록시)
```

### Docker 구성
- **개발 환경**: `docker-compose-dev.yml`
- **운영 환경**: `docker-compose-prod.yml`
- **다중 컨테이너**: 애플리케이션, 데이터베이스, 웹서버 분리

## 🚀 배포 및 운영

### AWS 인프라
- **VPC**: 네트워크 서브넷 및 보안 그룹 설정(예정)
- **EC2**: Docker Compose를 활용한 애플리케이션 배포
- **RDS**: MySQL 데이터베이스 연결(예정)
- **Route 53**: 커스텀 도메인 및 HTTPS 설정

### CI/CD 파이프라인
- **GitHub Actions**: 자동 빌드 및 배포
- **Docker 이미지 빌드**: 자동화된 컨테이너 빌드
- **배포 스크립트**: `deploy.sh`를 통한 원클릭 배포

## 📊 데이터베이스 설계

### ERD
<img width="793" alt="erd" src="https://github.com/user-attachments/assets/a0a4c11a-c502-4fe8-9973-606f0e9aa181">

### AWS 아키텍처
<img width="945" alt="aws아키" src="https://github.com/user-attachments/assets/44774cb0-678a-4600-a92c-1ca4935d1901">

## 📋 커밋 컨벤션
- **feat**: 새로운 기능 추가
- **fix**: 버그 수정
- **docs**: 문서 변경
- **style**: 코드 스타일 변경 (기능에 영향을 주지 않음)
- **refactor**: 코드 리팩토링 (기능 변화는 없고, 코드 개선)
- **chore**: 그 외 잡다한 작업 (빌드 도구, 패키지 관리자, 라이브러리 업데이트 등)
- **ci**: CI 설정 파일 수정
- **build**: 빌드 관련 파일 수정

## 🖼️ 프로젝트 스크린샷

<details>
<summary><b> ✅ 프로젝트 소개 펼치기</b></summary>
<div markdown="1">
  
### 🧷 랜딩 페이지
<img width="945" alt="111" src="https://github.com/user-attachments/assets/3b991d03-9ad9-4970-9f23-f488cd5d43df">
  
### 🧷 게시판 - 조회
<img width="945" alt="444" src="https://github.com/user-attachments/assets/623fbfca-81ee-4797-9b61-9b8d1c01ca06">
  
### 🧷 게시판 - 검색
<img width="945" alt="333" src="https://github.com/user-attachments/assets/f0387ce9-6d40-4a0e-957b-f6f70b78244a">

### 🧷 프로젝트 - 조회
<img width="945" alt="666" src="https://github.com/user-attachments/assets/668e00dc-676f-4780-9579-de4e559b9d16">  
  
### 🧷 프로젝트 - 검색
<img width="945" alt="555" src="https://github.com/user-attachments/assets/73809585-fdff-4046-9e39-383b6ced0923">

### 🧷 카페 찾기 검색  
<img width="945" alt="777" src="https://github.com/user-attachments/assets/828240d9-0a43-409a-9bfb-1993a9a7ffe7">

### 🧷 카페 찾기 검색결과 
<img width="945" alt="888" src="https://github.com/user-attachments/assets/3eca821d-d67f-463b-9a54-97f5144f17a2">

</div>
</details>

## 🔧 로컬 개발 환경 설정

### 필수 요구사항
- Docker & Docker Compose
- Java 11+
- Python 3.8+
- Node.js 14+

### 실행 방법
```bash
# 1. 프로젝트 클론
git clone [repository-url]
cd study

# 2. 개발 환경 실행
docker-compose -f docker-compose-dev.yml up -d

# 3. 애플리케이션 접속
# 메인 애플리케이션: http://localhost:8080
# Python API: http://localhost:8000
# Django Commerce: http://localhost:8001
```

---

**Let'Sadam** - 주니어 개발자의 성장 여정을 담은 프로젝트입니다. 🚀
