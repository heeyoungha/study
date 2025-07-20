import uvicorn
import asyncio
from database import async_engine, Base
from models import Diary, BookClubEntry
import os

async def init_db():
    """데이터베이스 테이블 초기화"""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("비동기 데이터베이스 테이블이 초기화되었습니다.")

async def main():
    """메인 함수 - DB 초기화 후 서버 시작"""
    await init_db()
    
    # uvicorn 서버 실행
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
        log_config=os.path.join(os.path.dirname(__file__), "log_config.yaml"),
        proxy_headers=True,
        forwarded_allow_ips="*"
    )

if __name__ == "__main__":
    asyncio.run(main()) 