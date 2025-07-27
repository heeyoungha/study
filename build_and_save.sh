#!/bin/bash
set -e

echo "1. 컨테이너 강제 정지 및 삭제"
# 강제 종료로 빠르게 내리기
docker-compose down --remove-orphans --timeout 10

echo "2. 남은 컨테이너 강제 삭제"
# 혹시 남은 컨테이너들 강제 삭제
docker ps -a --filter "name=study" --format "{{.ID}}" | xargs -r docker rm -f || true

echo "3. 사용된 볼륨 삭제"
docker volume rm study_mysql-data study_app-logs study_nginx-logs || true

echo "4. 기존 앱 이미지 삭제"
docker rmi -f study-app:latest || true

echo "4-1. 모든 study 관련 이미지 삭제"
docker images | grep study | awk '{print $3}' | xargs -r docker rmi -f || true

echo "5. 기존 빌드 결과물 정리"
rm -f build/libs/*.jar || true

echo "6. Gradle 빌드 실행"
./gradlew clean build -x test

echo "7. 이미지 빌드 및 컨테이너 실행"
docker-compose up --build -d

echo "8. 이미지 목록 확인"
docker image ls | grep -E 'study-app|mysql|nginx|python-api|django-commerce'

echo "9. 앱 이미지 태그 확인"
APP_IMAGE_TAG=$(docker images study-app:latest --format "table {{.Repository}}:{{.Tag}}" | tail -n +2)

if [ -z "$APP_IMAGE_TAG" ]; then
    echo "❌ study-app:latest 이미지를 찾을 수 없습니다."
    echo "사용 가능한 study-app 이미지:"
    docker images | grep study-app
    exit 1
fi

echo "10. 모든 이미지 하나로 저장"
docker save -o all_images.tar \
    "study-app:latest" \
    mysql:8.0 \
    django-commerce \
    python-api \
    nginx:alpine

echo "✅ 이미지 tar 저장 완료: all_images.tar"
