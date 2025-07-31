#!/bin/bash
set -e

echo "0. docker-compose.yml에서 latest로 빌드"
# docker-compose.yml은 latest로 유지

echo "1. 컨테이너 강제 정지 및 삭제"
# 강제 종료로 빠르게 내리기
docker-compose down --remove-orphans --timeout 10

echo "2. 남은 컨테이너 강제 삭제"
# 혹시 남은 컨테이너들 강제 삭제
docker ps -a --filter "name=study" --format "{{.ID}}" | xargs -r docker rm -f || true

echo "3. 사용된 볼륨 삭제"
docker volume rm study_mysql-data study_app-logs study_nginx-logs || true

echo "4. 기존 앱 이미지 삭제"
docker rmi -f study-app:latest study-app:latest || true

echo "4-1. 모든 study 관련 이미지 삭제"
docker images | grep study | awk '{print $3}' | xargs -r docker rmi -f || true

echo "5. 기존 빌드 결과물 정리"
rm -f build/libs/*.jar || true

echo "6. Gradle 빌드 실행"
./gradlew clean build -x test

echo "7. 이미지 빌드 및 컨테이너 실행"
docker-compose up --build -d

echo "8. 컨테이너 시작 대기"
echo "컨테이너들이 완전히 시작될 때까지 30초 대기..."
sleep 30

echo "9. Django Commerce 테스트 상품 생성"
# Django Commerce 컨테이너가 실행 중인지 확인
if docker ps | grep -q "django-commerce"; then
    echo "Django Commerce 컨테이너에서 테스트 상품 생성 중..."
    docker exec django-commerce python manage.py shell < django-commerce/commerce/create_test_products.py
    echo "✅ 테스트 상품 생성 완료"
else
    echo "⚠️ Django Commerce 컨테이너가 실행되지 않았습니다."
fi

echo "10. 이미지 목록 확인"
docker image ls | grep -E 'study-app|mysql|nginx|python-api|django-commerce'

echo "11. 컨테이너 상태 확인"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
