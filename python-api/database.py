import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

# .env 파일 로드 (DB 환경변수)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

DB_USER = os.getenv("DATASOURCE_USERNAME")
DB_PASSWORD = os.getenv("DATASOURCE_PASSWORD")
DB_HOST = os.getenv("DATASOURCE_HOST", "localhost")
DB_PORT = os.getenv("DATASOURCE_PORT", "3306")
DB_NAME = os.getenv("DATASOURCE_DB")

# 비동기 데이터베이스 URL (aiomysql 사용)
DATABASE_URL = f"mysql+aiomysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# 비동기 SQLAlchemy 엔진 및 세션 생성
async_engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    async_engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

# Base 클래스 정의
Base = declarative_base()

async def get_async_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()