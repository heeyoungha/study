import os
from sqlalchemy import create_engine
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

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# SQLAlchemy 엔진 및 세션 생성
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base 클래스 정의
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()