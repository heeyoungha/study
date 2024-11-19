# 📌 Let'Sadam 소개
-  주니어 개발자로서의 역량을 키우기 위해 설계한 로드맵을 구현해나가는 개인 프로젝트입니다. 
> [프로젝트 Todo-List 확인하기.](https://ceramic.notion.site/Todo-List-127366d1ed7180c4b107eab470e2080e?pvs=4)

## 📈 프로젝트 목표
- 체계적인 로드맵 구현을 통해 주니어 개발자로서의 역량 강화
- 클라우드 환경에서 배포 및 운영 경험 축적
- 최신 기술 도구와 프레임워크를 활용하여 실무에 가까운 프로젝트 구축

## 🛠 개발환경

### protocol Tool
- 인텔리J IDE

### 개발언어/framework
- JAVA, Spring/Spring boot/Spring Security, Jquery, BootStrap, JPA

### 데이터베이스
- MySQL (AWS RDS 사용)

### 서버 환경 및 배포 도구
- Docker (다중 컨테이너 구성)
- Linux (Ubuntu), Nginx
- AWS 구성 요소:
  - VPC: 네트워크 환경 설정
  - EC2: 애플리케이션 서버
  - RDS: MySQL 데이터베이스
  - Route 53: 도메인 관리 및 라우팅 설정

## 🔍 핵심 기능

### 0️⃣ 소셜 로그인
- OAuth2를 활용한 구글 소셜 로그인 기능

### 1️⃣ 게시판 CRUD
- 기본 게시판 기능 (글 작성, 수정, 삭제, 조회)
  - 게시글 검색하기 기능
  - 페이지네이션 기능

### 2️⃣ 외부 api 호출
- 카카오 주소 API를 사용하여 외부 데이터와 연동

### 4️⃣ Docker 다중 컨테이너 구현
- 애플리케이션과 데이터베이스, nginx 컨테이너를 분리하여 구성

### 5️⃣ aws 기반 배포
- VPC: 네트워크 서브넷 및 보안 그룹 설정
- EC2: Docker Compose를 활용한 애플리케이션 배포
- RDS: MySQL 데이터베이스 연결
- Route 53: 커스텀 도메인 및 HTTPS 설정

### 6️⃣ CI / CD 자동화
- GitHub Actions를 사용한 빌드 및 배포 자동화

## 🗞️ ERD & AWS 아키텍처
- ERD

<img width="793" alt="erd" src="https://github.com/user-attachments/assets/a0a4c11a-c502-4fe8-9973-606f0e9aa181">

- AWS 아키텍처

<img width="945" alt="aws아키" src="https://github.com/user-attachments/assets/44774cb0-678a-4600-a92c-1ca4935d1901">

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
  
