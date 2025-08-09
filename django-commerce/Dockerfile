FROM node:18-alpine AS frontend-builder

# React 빌드 단계
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci --only=production

COPY frontend/ .
RUN npm run build

FROM python:3.10-slim

WORKDIR /app

# 시스템 패키지 업데이트 및 필요한 패키지 설치
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    pkg-config \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Python 의존성 설치
COPY commerce/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Django 프로젝트 복사
COPY commerce/ .

# React 빌드 파일들을 frontend/build 디렉토리에 복사 (entrypoint.sh에서 사용)
COPY --from=frontend-builder /app/frontend/build/ ./frontend/build/

# Entrypoint 스크립트 복사 및 실행 권한 부여
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# 포트 노출
EXPOSE 8000

# Entrypoint 스크립트 실행
CMD ["/entrypoint.sh"] 