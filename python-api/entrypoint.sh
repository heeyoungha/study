#!/bin/bash

# 데이터베이스 연결 대기
echo "데이터베이스 연결을 기다리는 중..."
sleep 10

# 비동기 서버 실행
echo "비동기 FastAPI 서버를 시작합니다..."
python run_async_server.py 