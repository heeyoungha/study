#!/bin/bash

# 데이터베이스 연결 대기
echo "Waiting for database..."
while ! nc -z mysql 3306; do
  sleep 1
done
echo "Database is ready!"

# Django 마이그레이션 실행
echo "Running Django migrations..."
python manage.py migrate

# 정적 파일 수집
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Django 서버 시작
echo "Starting Django server..."
python manage.py runserver 0.0.0.0:8000 