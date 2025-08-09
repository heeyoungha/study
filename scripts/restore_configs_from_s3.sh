#!/bin/bash

# S3에서 설정 파일 및 버전 정보를 복구하는 스크립트

set -e

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}🔄 S3에서 설정 파일 및 버전 정보 복구 시작${NC}"

# .env 파일 로드
if [ -f ".env" ]; then
    echo -e "${BLUE}📁 .env 파일 로드 중...${NC}"
    export $(cat .env | grep -v '^#' | xargs)
    echo "✅ .env 파일 로드 완료"
fi

# S3 버킷 이름 확인
if [ -z "$AWS_STORAGE_BUCKET_NAME" ]; then
    echo -e "${YELLOW}⚠️  AWS_STORAGE_BUCKET_NAME 환경변수가 설정되지 않았습니다.${NC}"
    echo "환경변수를 설정하거나 직접 입력해주세요:"
    read -p "S3 버킷 이름을 입력하세요: " AWS_STORAGE_BUCKET_NAME
fi

# AWS 리전 설정 (기본값: ap-northeast-2)
AWS_S3_REGION_NAME=${AWS_S3_REGION_NAME:-ap-northeast-2}

# IAM 역할 확인
echo -e "${YELLOW}🔐 IAM 역할 확인 중...${NC}"
if aws sts get-caller-identity &> /dev/null; then
    echo -e "${GREEN}✅ IAM 역할이 정상적으로 설정되어 있습니다.${NC}"
    aws sts get-caller-identity
else
    echo -e "${RED}❌ IAM 역할을 확인할 수 없습니다.${NC}"
    echo "EC2 인스턴스에 IAM 역할이 올바르게 설정되어 있는지 확인하세요."
    exit 1
fi

# S3에서 사용 가능한 백업 목록 확인
echo -e "${YELLOW}🔍 S3에서 사용 가능한 백업 목록 확인 중...${NC}"
aws s3 ls "s3://$AWS_STORAGE_BUCKET_NAME/configs/" --recursive --human-readable

# 복구할 백업 선택
echo -e "${BLUE}📋 복구할 백업을 선택하세요:${NC}"
echo "1. 최신 백업 자동 복구"
echo "2. 특정 백업 선택"
read -p "선택 (1 또는 2): " choice

if [ "$choice" = "2" ]; then
    echo -e "${YELLOW}사용 가능한 백업 목록:${NC}"
    aws s3 ls "s3://$AWS_STORAGE_BUCKET_NAME/configs/" | grep "^PRE" | awk '{print $2}' | sed 's/\///'
    read -p "복구할 백업 폴더명을 입력하세요: " backup_folder
    S3_SOURCE="s3://$AWS_STORAGE_BUCKET_NAME/configs/$backup_folder"
else
    # 최신 백업 자동 선택
    echo -e "${YELLOW}최신 백업을 자동으로 찾는 중...${NC}"
    latest_backup=$(aws s3 ls "s3://$AWS_STORAGE_BUCKET_NAME/configs/" | grep "^PRE" | awk '{print $2}' | sort | tail -1)
    if [ -z "$latest_backup" ]; then
        echo -e "${RED}❌ 사용 가능한 백업이 없습니다.${NC}"
        exit 1
    fi
    S3_SOURCE="s3://$AWS_STORAGE_BUCKET_NAME/configs/$latest_backup"
    echo -e "${GREEN}✅ 최신 백업 선택: $latest_backup${NC}"
fi

# 복구 디렉토리 생성
RESTORE_DIR="restored_configs_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$RESTORE_DIR"

echo -e "${BLUE}📁 복구 디렉토리 생성: $RESTORE_DIR${NC}"

# S3에서 백업 파일 다운로드
echo -e "${YELLOW}📥 S3에서 백업 파일 다운로드 중...${NC}"
aws s3 cp "$S3_SOURCE" "$RESTORE_DIR" --recursive

# 복구된 파일 목록 확인
echo -e "${GREEN}✅ 복구 완료!${NC}"
echo -e "${BLUE}📋 복구된 파일 목록:${NC}"
find "$RESTORE_DIR" -type f | sort

# 백업 정보 파일 확인
if [ -f "$RESTORE_DIR/backup-info.txt" ]; then
    echo -e "${BLUE}📝 백업 정보:${NC}"
    cat "$RESTORE_DIR/backup-info.txt"
fi

# 복구 옵션 제공
echo -e "${YELLOW}🔄 복구 옵션을 선택하세요:${NC}"
echo "1. 파일만 복구 (수동으로 복사)"
echo "2. 자동으로 원래 위치에 복구 (주의: 기존 파일 덮어씀)"
read -p "선택 (1 또는 2): " restore_choice

if [ "$restore_choice" = "2" ]; then
    echo -e "${RED}⚠️  경고: 기존 파일이 덮어써집니다!${NC}"
    read -p "계속하시겠습니까? (y/N): " confirm
    
    if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
        echo -e "${YELLOW}🔄 파일을 원래 위치에 복구 중...${NC}"
        
        # Docker 설정 파일 복구
        if [ -f "$RESTORE_DIR/docker-compose.yml" ]; then
            cp "$RESTORE_DIR/docker-compose.yml" ./
            echo "✅ docker-compose.yml 복구 완료"
        fi
        
        if [ -f "$RESTORE_DIR/docker-compose-dev.yml" ]; then
            cp "$RESTORE_DIR/docker-compose-dev.yml" ./
            echo "✅ docker-compose-dev.yml 복구 완료"
        fi
        
        if [ -f "$RESTORE_DIR/docker-compose-prod.yml" ]; then
            cp "$RESTORE_DIR/docker-compose-prod.yml" ./
            echo "✅ docker-compose-prod.yml 복구 완료"
        fi
        
        # 환경 변수 파일 복구
        if [ -f "$RESTORE_DIR/.env" ]; then
            cp "$RESTORE_DIR/.env" ./
            echo "✅ .env 복구 완료"
        fi
        
        # Nginx 설정 파일 복구
        if [ -d "$RESTORE_DIR/nginx" ]; then
            cp -r "$RESTORE_DIR/nginx/" ./
            echo "✅ Nginx 설정 복구 완료"
        fi
        
        # Django 설정 파일 복구
        if [ -d "$RESTORE_DIR/django-commerce" ]; then
            cp -r "$RESTORE_DIR/django-commerce/" ./
            echo "✅ Django 설정 복구 완료"
        fi
        
        # Python API 설정 파일 복구
        if [ -d "$RESTORE_DIR/python-api" ]; then
            cp -r "$RESTORE_DIR/python-api/" ./
            echo "✅ Python API 설정 복구 완료"
        fi
        
        # Spring Boot 설정 파일 복구
        if [ -d "$RESTORE_DIR/spring-boot" ]; then
            cp -r "$RESTORE_DIR/spring-boot/" ./
            echo "✅ Spring Boot 설정 복구 완료"
        fi
        
        # Docker 이미지 복구 안내
        if [ -d "$RESTORE_DIR/docker-images" ]; then
            echo "✅ Docker 이미지 tar 파일 복구 완료"
            echo "📋 Docker 이미지 복구 방법:"
            echo "   cd $RESTORE_DIR/docker-images"
            echo "   docker load -i [이미지명].tar"
        fi
        
        echo -e "${GREEN}✅ 모든 파일이 원래 위치에 복구되었습니다!${NC}"
    else
        echo -e "${YELLOW}자동 복구가 취소되었습니다.${NC}"
    fi
else
    echo -e "${BLUE}📁 파일이 $RESTORE_DIR에 복구되었습니다.${NC}"
    echo "수동으로 필요한 파일을 원하는 위치에 복사하세요."
fi

echo -e "${GREEN}🎉 복구 작업이 완료되었습니다!${NC}"
echo -e "${BLUE}📁 복구된 파일 위치: $RESTORE_DIR${NC}" 