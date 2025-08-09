#!/bin/bash

# 설정 파일 및 버전 정보를 S3에 백업하는 스크립트

set -e

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}🔄 설정 파일 및 버전 정보 백업 시작${NC}"

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

# 백업 디렉토리 생성
BACKUP_DIR="config_backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

echo -e "${BLUE}📁 백업 디렉토리 생성: $BACKUP_DIR${NC}"

# 백업 정보 파일 생성
echo "백업 생성 시간: $(date)" > "$BACKUP_DIR/backup-info.txt"
echo "백업 생성자: $(whoami)" >> "$BACKUP_DIR/backup-info.txt"
echo "호스트명: $(hostname)" >> "$BACKUP_DIR/backup-info.txt"
echo "Git 커밋 해시: $(git rev-parse HEAD 2>/dev/null || echo 'Git 정보 없음')" >> "$BACKUP_DIR/backup-info.txt"
echo "Git 브랜치: $(git branch --show-current 2>/dev/null || echo 'Git 정보 없음')" >> "$BACKUP_DIR/backup-info.txt"
echo "Docker 버전: $(docker --version 2>/dev/null || echo 'Docker 정보 없음')" >> "$BACKUP_DIR/backup-info.txt"

# Docker 설정 파일 백업
echo -e "${YELLOW}🐳 Docker 설정 파일 백업 중...${NC}"
if [ -f "docker-compose.yml" ]; then
    cp docker-compose.yml "$BACKUP_DIR/"
    echo "✅ docker-compose.yml 백업 완료"
fi

if [ -f "docker-compose-dev.yml" ]; then
    cp docker-compose-dev.yml "$BACKUP_DIR/"
    echo "✅ docker-compose-dev.yml 백업 완료"
fi

if [ -f "docker-compose-prod.yml" ]; then
    cp docker-compose-prod.yml "$BACKUP_DIR/"
    echo "✅ docker-compose-prod.yml 백업 완료"
fi

# 환경 변수 파일 백업
echo -e "${YELLOW}🔧 환경 변수 파일 백업 중...${NC}"
if [ -f ".env" ]; then
    cp .env "$BACKUP_DIR/"
    echo "✅ .env 백업 완료"
fi

if [ -f ".env.local" ]; then
    cp .env.local "$BACKUP_DIR/"
    echo "✅ .env.local 백업 완료"
fi

if [ -f ".env.production" ]; then
    cp .env.production "$BACKUP_DIR/"
    echo "✅ .env.production 백업 완료"
fi

# Nginx 설정 파일 백업
echo -e "${YELLOW}🌐 Nginx 설정 파일 백업 중...${NC}"
if [ -d "nginx" ]; then
    cp -r nginx "$BACKUP_DIR/"
    echo "✅ Nginx 설정 백업 완료"
fi

# Django 설정 파일 백업
echo -e "${YELLOW}🐍 Django 설정 파일 백업 중...${NC}"
if [ -d "django-commerce" ]; then
    # 민감한 정보 제외하고 백업
    mkdir -p "$BACKUP_DIR/django-commerce"
    
    # 주요 설정 파일만 백업
    if [ -f "django-commerce/settings.py" ]; then
        cp django-commerce/settings.py "$BACKUP_DIR/django-commerce/"
    fi
    
    if [ -f "django-commerce/requirements.txt" ]; then
        cp django-commerce/requirements.txt "$BACKUP_DIR/django-commerce/"
    fi
    
    if [ -d "django-commerce/store" ]; then
        cp -r django-commerce/store "$BACKUP_DIR/django-commerce/"
    fi
    
    if [ -d "django-commerce/templates" ]; then
        cp -r django-commerce/templates "$BACKUP_DIR/django-commerce/"
    fi
    
    echo "✅ Django 설정 백업 완료"
fi

# Python API 설정 파일 백업
echo -e "${YELLOW}🐍 Python API 설정 파일 백업 중...${NC}"
if [ -d "python-api" ]; then
    mkdir -p "$BACKUP_DIR/python-api"
    
    # 주요 설정 파일만 백업
    if [ -f "python-api/app.py" ]; then
        cp python-api/app.py "$BACKUP_DIR/python-api/"
    fi
    
    if [ -f "python-api/requirements.txt" ]; then
        cp python-api/requirements.txt "$BACKUP_DIR/python-api/"
    fi
    
    if [ -f "python-api/database.py" ]; then
        cp python-api/database.py "$BACKUP_DIR/python-api/"
    fi
    
    if [ -d "python-api/routes" ]; then
        cp -r python-api/routes "$BACKUP_DIR/python-api/"
    fi
    
    if [ -d "python-api/templates" ]; then
        cp -r python-api/templates "$BACKUP_DIR/python-api/"
    fi
    
    echo "✅ Python API 설정 백업 완료"
fi

# Spring Boot 설정 파일 백업
echo -e "${YELLOW}☕ Spring Boot 설정 파일 백업 중...${NC}"
if [ -d "src/main/resources" ]; then
    mkdir -p "$BACKUP_DIR/spring-boot"
    
    # 주요 설정 파일만 백업
    if [ -f "src/main/resources/application.yml" ]; then
        cp src/main/resources/application.yml "$BACKUP_DIR/spring-boot/"
    fi
    
    if [ -f "build.gradle" ]; then
        cp build.gradle "$BACKUP_DIR/spring-boot/"
    fi
    
    if [ -f "settings.gradle" ]; then
        cp settings.gradle "$BACKUP_DIR/spring-boot/"
    fi
    
    echo "✅ Spring Boot 설정 백업 완료"
fi

# Docker 이미지 백업 (tar 파일로 저장)
echo -e "${YELLOW}🐳 Docker 이미지 백업 중...${NC}"
mkdir -p "$BACKUP_DIR/docker-images"

# docker-compose-prod.yml에서 사용하는 이미지들 추출 및 백업
if [ -f "docker-compose-prod.yml" ]; then
    echo "docker-compose-prod.yml에서 이미지 정보 추출 중..."
    
    # 이미지 목록 추출
    IMAGES=($(grep -E "^[[:space:]]*image:" docker-compose-prod.yml | sed 's/.*image:[[:space:]]*//' | tr -d '"'))
    
    for image in "${IMAGES[@]}"; do
        if [ -n "$image" ]; then
            echo "이미지 백업 중: $image"
            
            # 이미지가 로컬에 존재하는지 확인
            if docker image inspect "$image" &> /dev/null; then
                # tar 파일로 저장
                tar_filename=$(echo "$image" | tr ':/' '_' | tr -d ' ').tar
                docker save "$image" -o "$BACKUP_DIR/docker-images/$tar_filename"
                echo "✅ $image -> $tar_filename 백업 완료"
            else
                echo "⚠️  이미지 $image가 로컬에 존재하지 않습니다."
            fi
        fi
    done
    
    # 외부 이미지들도 백업 (grafana, fluent-bit 등)
    EXTERNAL_IMAGES=("grafana/grafana:10.0.0" "grafana/loki:2.8.0" "fluent/fluent-bit:2.1.10")
    
    for ext_image in "${EXTERNAL_IMAGES[@]}"; do
        echo "외부 이미지 백업 중: $ext_image"
        
        # 이미지가 로컬에 존재하는지 확인
        if docker image inspect "$ext_image" &> /dev/null; then
            tar_filename=$(echo "$ext_image" | tr ':/' '_' | tr -d ' ').tar
            docker save "$ext_image" -o "$BACKUP_DIR/docker-images/$tar_filename"
            echo "✅ $ext_image -> $tar_filename 백업 완료"
        else
            echo "⚠️  이미지 $ext_image가 로컬에 존재하지 않습니다."
        fi
    done
    
    # 백업된 이미지 목록을 백업 정보에 추가
    echo "" >> "$BACKUP_DIR/backup-info.txt"
    echo "=== 백업된 Docker 이미지 목록 ===" >> "$BACKUP_DIR/backup-info.txt"
    for image in "${IMAGES[@]}"; do
        if [ -n "$image" ]; then
            echo "- $image" >> "$BACKUP_DIR/backup-info.txt"
        fi
    done
    echo "" >> "$BACKUP_DIR/backup-info.txt"
    echo "=== 백업된 외부 이미지 목록 ===" >> "$BACKUP_DIR/backup-info.txt"
    for ext_image in "${EXTERNAL_IMAGES[@]}"; do
        echo "- $ext_image" >> "$BACKUP_DIR/backup-info.txt"
    done
    
    echo "✅ Docker 이미지 백업 완료"
else
    echo "⚠️  docker-compose-prod.yml 파일을 찾을 수 없습니다."
fi

# 기타 중요 설정 파일 백업
echo -e "${YELLOW}📋 기타 중요 설정 파일 백업 중...${NC}"

# 배포 스크립트
if [ -f "deploy.sh" ]; then
    cp deploy.sh "$BACKUP_DIR/"
    echo "✅ deploy.sh 백업 완료"
fi

if [ -f "deploy-prod.sh" ]; then
    cp deploy-prod.sh "$BACKUP_DIR/"
    echo "✅ deploy-prod.sh 백업 완료"
fi

if [ -f "start.sh" ]; then
    cp start.sh "$BACKUP_DIR/"
    echo "✅ start.sh 백업 완료"
fi

if [ -f "start_local_dev.sh" ]; then
    cp start_local_dev.sh "$BACKUP_DIR/"
    echo "✅ start_local_dev.sh 백업 완료"
fi

# 데이터베이스 설정
if [ -d "database" ]; then
    cp -r database "$BACKUP_DIR/"
    echo "✅ 데이터베이스 설정 백업 완료"
fi

# 모니터링 설정
if [ -f "fluent-bit.conf" ]; then
    cp fluent-bit.conf "$BACKUP_DIR/"
    echo "✅ fluent-bit.conf 백업 완료"
fi

if [ -f "loki-config.yaml" ]; then
    cp loki-config.yaml "$BACKUP_DIR/"
    echo "✅ loki-config.yaml 백업 완료"
fi

# 백업 파일 목록 생성
echo -e "${BLUE}📋 백업된 파일 목록:${NC}"
find "$BACKUP_DIR" -type f | sort > "$BACKUP_DIR/backup-file-list.txt"
cat "$BACKUP_DIR/backup-file-list.txt"

# 백업 크기 확인
BACKUP_SIZE=$(du -sh "$BACKUP_DIR" | cut -f1)
echo -e "${BLUE}📊 백업 크기: $BACKUP_SIZE${NC}"

# S3에 백업 업로드
echo -e "${YELLOW}📤 S3에 백업 업로드 중...${NC}"
S3_DEST="s3://$AWS_STORAGE_BUCKET_NAME/configs/$(basename $BACKUP_DIR)/"

aws s3 cp "$BACKUP_DIR" "$S3_DEST" --recursive

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ S3 백업 업로드 완료!${NC}"
    echo -e "${BLUE}📍 S3 위치: $S3_DEST${NC}"
    
    # S3에 업로드된 파일 확인
    echo -e "${BLUE}🔍 S3에 업로드된 파일 확인:${NC}"
    aws s3 ls "$S3_DEST" --recursive --human-readable
else
    echo -e "${RED}❌ S3 백업 업로드 실패${NC}"
    exit 1
fi

# 로컬 백업 디렉토리 정리 옵션
echo -e "${YELLOW}🧹 로컬 백업 디렉토리 정리 옵션:${NC}"
echo "1. 로컬 백업 디렉토리 유지"
echo "2. 로컬 백업 디렉토리 삭제"
read -p "선택 (1 또는 2): " cleanup_choice

if [ "$cleanup_choice" = "2" ]; then
    echo -e "${YELLOW}🗑️  로컬 백업 디렉토리 삭제 중...${NC}"
    rm -rf "$BACKUP_DIR"
    echo -e "${GREEN}✅ 로컬 백업 디렉토리 삭제 완료${NC}"
else
    echo -e "${BLUE}📁 로컬 백업 디렉토리 유지: $BACKUP_DIR${NC}"
fi

echo -e "${GREEN}🎉 백업 작업이 완료되었습니다!${NC}"
echo -e "${BLUE}📍 S3 백업 위치: $S3_DEST${NC}"
echo -e "${BLUE}📊 백업 크기: $BACKUP_SIZE${NC}"
echo -e "${BLUE}📅 백업 시간: $(date)${NC}" 