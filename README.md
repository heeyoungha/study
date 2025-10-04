# 📌 ActLog 소개
-  주니어 개발자로서의 역량을 키우기 위해 설계한 로드맵을 구현해나가는 개인 프로젝트입니다.
-  url : https://letsadam.shop

## 📈 프로젝트 목표
- 체계적인 로드맵 구현을 통해 주니어 개발자로서의 역량 강화
- 클라우드 환경에서 배포 및 운영 경험 축적
- 최신 기술 도구와 프레임워크를 활용하여 실무에 가까운 프로젝트 구축

## 🛠 개발환경

### protocol Tool
- Visual Studio COde
- 인텔리J IDE

### 개발언어/framework
- **Backend**: JAVA, Spring/Spring Boot/Spring Security, JPA
- **Frontend**: JQuery, Bootstrap, Thymeleaf
- **Python API**: FastAPI, SQLAlchemy, Alembic
- **Django Commerce**: Django, Django REST Framework

### 데이터베이스
- MySQL 

### 서버 환경 및 배포 도구
- **Container**: Docker (다중 컨테이너 구성)
- **Web Server**: Nginx (리버스 프록시)
- **OS**: Linux
- **AWS 구성 요소**:
    - VPC: 네트워크 환경 설정 (예정)
    - EC2: 애플리케이션 서버
    - RDS: MySQL 데이터베이스 (예정)
    - Route 53: 도메인 관리 및 라우팅 설정
    - SSL: Let's Encrypt 인증서

## 🔍 핵심 기능

### 0️⃣ 소셜 로그인
- OAuth2를 활용한 구글 소셜 로그인 기능

### 1️⃣ 게시판 CRUD
- 기본 게시판 기능 (글 작성, 수정, 삭제, 조회)
    - 게시글 검색하기 기능
    - 페이지네이션 기능

### 2️⃣ 외부 API 호출
- 카카오 주소 API를 사용하여 외부 데이터와 연동
- 카카오 장소 검색 API를 활용한 카페 추천 시스템

### 3️⃣ 일기/북클럽 시스템 (Python FastAPI)
- **일기 기능**: 
  - 일기 작성, 조회, 수정, 삭제
  - GPT를 활용한 일기 요약 및 감정 분석
  - 일기 목록 조회 및 검색
- **북클럽 기능**:
  - 독서 기록 작성 및 관리
  - GPT를 활용한 독서 요약 및 분석
  - 북클럽 참여자 관리

### 4️⃣ Django Commerce (전자상거래)
- **상품 관리**: 상품 등록, 수정, 삭제
- **장바구니**: 상품 추가, 수량 변경, 삭제
- **주문 시스템**: 주문 생성, 결제 처리
- **관리자 기능**: 주문 관리, 재고 관리

### 5️⃣ Docker 다중 컨테이너 구현
- **Spring Boot**: 메인 애플리케이션
- **Python FastAPI**: 일기/북클럽 API
- **Django**: 전자상거래 시스템
- **MySQL**: 데이터베이스
- **Nginx**: 리버스 프록시 및 정적 파일 서빙

### 6️⃣ AWS 기반 배포
- **VPC**: 네트워크 서브넷 및 보안 그룹 설정
- **EC2**: Docker Compose를 활용한 애플리케이션 배포
- **RDS**: MySQL 데이터베이스 연결
- **Route 53**: 커스텀 도메인 및 HTTPS 설정
- **SSL**: Let's Encrypt 자동 인증서 갱신

### 7️⃣ CI/CD 자동화
- GitHub Actions를 사용한 빌드 및 배포 자동화
- Docker 이미지 빌드 및 태그 관리
- 자동 테스트 및 배포 파이프라인

### 8️⃣ 데이터 영속성
- Docker 볼륨을 활용한 데이터베이스 데이터 보존
- 컨테이너 재시작 시에도 데이터 유지
- 로그 파일 및 업로드 파일 보존

## 🏗️ 프로젝트 구조

```
study/
├── src/main/java/com/example/study/     # Spring Boot 애플리케이션
├── python-api/                          # Python FastAPI (일기/북클럽)
│   ├── routes/                          # API 라우트
│   ├── models.py                        # 데이터베이스 모델
│   └── templates/                       # HTML 템플릿
├── django-commerce/                      # Django Commerce
│   ├── store/                           # 상점 앱
│   └── templates/                       # HTML 템플릿
├── nginx/                               # Nginx 설정
├── database/                            # MySQL 설정
└── docker-compose-*.yml                 # Docker Compose 설정
```

<!-- ## 🗞️ ERD & AWS 아키텍처
- ERD

<img width="793" alt="erd" src="https://github.com/user-attachments/assets/a0a4c11a-c502-4fe8-9973-606f0e9aa181">

- AWS 아키텍처

<img width="945" alt="aws아키" src="https://github.com/user-attachments/assets/44774cb0-678a-4600-a92c-1ca4935d1901"> -->

## ETC

- 커밋 컨벤션
    - feat: 새로운 기능 추가
    - fix: 버그 수정
    - docs: 문서 변경
    - style: 코드 스타일 변경 (기능에 영향을 주지 않음)
    - refactor: 코드 리팩토링 (기능 변화는 없고, 코드 개선)
    - chore: 그 외 잡다한 작업 (빌드 도구, 패키지 관리자, 라이브러리 업데이트 등)
    - ci: CI 설정 파일 수정
    - build: 빌드 관련 파일 수정

<br>
<!-- 
<details>
<summary><b> ✅ 프로젝트 소개 펼치기</b></summary>
<div markdown="1">
  🧷 랜딩 페이지

<img width="945" alt="111" src="https://github.com/user-attachments/assets/3b991d03-9ad9-4970-9f23-f488cd5d43df">

🧷 게시판 - 조회

<img width="945" alt="444" src="https://github.com/user-attachments/assets/623fbfca-81ee-4797-9b61-9b8d1c01ca06">

🧷 게시판 - 검색

<img width="945" alt="333" src="https://github.com/user-attachments/assets/f0387ce9-6d40-4a0e-957b-f6f70b78244a">

🧷 프로젝트 - 조회

<img width="945" alt="666" src="https://github.com/user-attachments/assets/668e00dc-676f-4780-9579-de4e559b9d16">  

🧷 프로젝트 - 검색

<img width="945" alt="555" src="https://github.com/user-attachments/assets/73809585-fdff-4046-9e39-383b6ced0923">

🧷 카페 찾기 검색

<img width="945" alt="777" src="https://github.com/user-attachments/assets/828240d9-0a43-409a-9bfb-1993a9a7ffe7">

🧷 카페 찾기 검색결과

<img width="945" alt="888" src="https://github.com/user-attachments/assets/3eca821d-d67f-463b-9a54-97f5144f17a2">

🧷 일기 작성 페이지

<img width="945" alt="diary-form" src="https://github.com/user-attachments/assets/diary-form-screenshot">

🧷 일기 목록 페이지

<img width="945" alt="diary-list" src="https://github.com/user-attachments/assets/diary-list-screenshot">

🧷 북클럽 기록 작성

<img width="945" alt="bookclub-form" src="https://github.com/user-attachments/assets/bookclub-form-screenshot">

🧷 Django Commerce 상품 목록

<img width="945" alt="commerce-products" src="https://github.com/user-attachments/assets/commerce-products-screenshot">




</div>
</details> -->
