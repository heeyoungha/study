#!/bin/bash

echo "=== DEPLOY.SH - Production Deployment ==="
echo "Current directory: $(pwd)"

echo "=== Creating required directories ==="
# 로그 디렉토리 생성
mkdir -p logs/app logs/nginx logs/django

# 데이터 디렉토리 생성
mkdir -p data/mysql

# Django 디렉토리 생성
mkdir -p django-commerce/media django-commerce/staticfiles

echo "=== Setting directory permissions ==="
# MySQL 데이터 디렉토리 권한 설정 (MySQL 사용자: 999)
sudo chown -R 999:999 data/mysql 2>/dev/null || echo "Warning: Could not set MySQL directory permissions"

# 로그 디렉토리 권한 설정
chmod -R 755 logs/
chmod -R 755 data/

# Django 디렉토리 권한 설정
chmod -R 755 django-commerce/media
chmod -R 755 django-commerce/staticfiles

echo "=== Directory structure created ==="
echo "Directories created:"
echo "- logs/app (Spring Boot logs)"
echo "- logs/nginx (Nginx logs)"
echo "- logs/django (Django logs)"
echo "- data/mysql (MySQL data)"
echo "- django-commerce/media (Django media files)"
echo "- django-commerce/staticfiles (Django static files)"

echo "=== Starting Docker Compose ==="
# 기존 컨테이너 정리
docker-compose down

# 이미지 빌드
docker-compose build

# 컨테이너 시작
docker-compose up -d

echo "=== Deployment completed ==="
echo "Services started:"
echo "- Spring Boot (port 8080)"
echo "- FastAPI (port 8000)"
echo "- Django (port 8002)"
echo "- MySQL (port 3306)"
echo "- Nginx (ports 80, 443)"

echo "=== Health check ==="
sleep 10
docker-compose ps

echo "=== Logs ==="
echo "To view logs: docker-compose logs -f"
echo "To view specific service logs: docker-compose logs -f [service-name]" 