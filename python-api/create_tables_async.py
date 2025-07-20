import asyncio
from database import async_engine, Base
from models import Diary, BookClubEntry

async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("비동기 데이터베이스 테이블이 생성되었습니다.")

if __name__ == "__main__":
    asyncio.run(create_tables()) 