from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from service import analyze_sentiment, recommendation_map, save_diary, get_all_diaries
from schemas import DiaryRequest, DiaryResponse, DiaryListResponse, DiaryListItem
from database import SessionLocal

import os

templates = Jinja2Templates(directory="templates")

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- 화면용 라우트 ---
@router.get("/diary", response_class=HTMLResponse)
def diary_form(request: Request):
    return templates.TemplateResponse("diary/diary-form.html", {"request": request})

@router.post("/diary", response_class=HTMLResponse)
def diary_submit(request: Request, text: str = Form(...), db: Session = Depends(get_db)):
    sentiment = analyze_sentiment(text)
    recommendations = recommendation_map.get(sentiment, recommendation_map["neutral"])
    save_diary(db, text, sentiment, recommendations)
    return templates.TemplateResponse(
        "diary/diary-result.html",
        {"request": request, "text": text, "sentiment": sentiment, "recommendations": recommendations}
    )

@router.get("/diary/list", response_class=HTMLResponse)
def diary_list(request: Request, db: Session = Depends(get_db)):
    diaries = get_all_diaries(db)
    return templates.TemplateResponse(
        "diary/diary-list.html",
        {"request": request, "diaries": diaries}
    )