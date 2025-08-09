#!/bin/bash

# 데이터베이스 호스트 설정 (운영 환경에서는 RDS 엔드포인트)
DB_HOST=${DB_HOST:-mysql}
RDS_ENDPOINT=${RDS_ENDPOINT:-}
DB_PORT=${DB_PORT:-3306}

# 데이터베이스 연결 대기 (DB_HOST 먼저 시도, 실패시 RDS_ENDPOINT 시도)
echo "Trying to connect to database at $DB_HOST:$DB_PORT..."

# DB_HOST로 먼저 시도
if nc -z $DB_HOST $DB_PORT 2>/dev/null; then
    echo "Database connection successful at $DB_HOST:$DB_PORT"
else
    echo "Connection to $DB_HOST:$DB_PORT failed"
    
    # RDS_ENDPOINT가 설정되어 있으면 시도
    if [ -n "$RDS_ENDPOINT" ]; then
        echo "Trying RDS endpoint: $RDS_ENDPOINT:$DB_PORT"
        while ! nc -z $RDS_ENDPOINT $DB_PORT; do
            sleep 1
        done
        echo "RDS database connection successful at $RDS_ENDPOINT:$DB_PORT"
    else
        echo "RDS_ENDPOINT not set, waiting for $DB_HOST:$DB_PORT"
        while ! nc -z $DB_HOST $DB_PORT; do
            sleep 1
        done
        echo "Database is ready at $DB_HOST:$DB_PORT"
    fi
fi

# Django 마이그레이션 실행
echo "Running Django migrations..."
python manage.py migrate

# 정적 파일 수집 (React 빌드 파일 포함)
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# React 빌드 파일들을 staticfiles로 복사 (collectstatic 후에)
echo "Copying React build files to staticfiles..."
cp -r ./frontend/build/* ./staticfiles/

# Django 서버 시작
echo "Starting Django server..."
python manage.py runserver 0.0.0.0:8000 