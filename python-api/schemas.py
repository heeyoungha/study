from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from datetime import date

class DiaryRequest(BaseModel):
    text: str

class DiaryResponse(BaseModel):
    sentiment: str
    recommendations: List[str]

class DiaryListItem(BaseModel):
    id: int
    text: str
    sentiment: str
    created_at: datetime

class DiaryListResponse(BaseModel):
    diaries: List[DiaryListItem] 

class DiaryCreate(BaseModel):
    text: str
    recommended_projects: Optional[List[str]] = None

class DiaryRead(BaseModel):
    id: int
    text: str
    sentiment: str
    created_at: datetime
    recommended_projects: Optional[List[str]] = None 

class BookClubEntryCreate(BaseModel):
    date: date
    book_title: str
    review: str
    summary: str

class BookClubEntryResponse(BaseModel):
    id: int
    date: date
    book_title: str
    review: str
    summary: str
    recommended_projects: List[str]

    class Config:
        orm_mode = True 