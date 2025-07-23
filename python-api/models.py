from sqlalchemy import Column, Integer, String, Date, Text, Boolean, DateTime
from database import Base

class Diary(Base):
    __tablename__ = "diary"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    content = Column(Text)
    summary = Column(String(255))  
    sentiment = Column(String(16)) 
    recommended_projects = Column(Text)  # JSON 문자열로 저장
    user_id = Column(Integer, nullable=True)  # 작성자 ID

class BookClubEntry(Base):
    __tablename__ = "bookclub_entry"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    book_title = Column(String(255))
    review = Column(Text)
    summary = Column(String(255))  # 한줄소감
    recommended_projects = Column(Text)  # JSON 문자열로 저장 
    user_id = Column(Integer, nullable=True)  # 작성자 ID 

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255))
    email = Column(String(255))
    role = Column(String(255))
    pw = Column(String(255))
    is_deleted = Column(Boolean, default=False)
    created_date = Column(DateTime)
    modified_date = Column(DateTime)
    project_user_id = Column(Integer, nullable=True) 