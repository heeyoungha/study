from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from service import analyze_sentiment, recommendation_map, save_diary, get_all_diaries
from schemas import DiaryCreate, DiaryRead
from database import SessionLocal
from models import Diary
import os

templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), '../templates'))

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/diary", response_class=HTMLResponse)
def diary_form(request: Request):
    return templates.TemplateResponse("diary/diary-form.html", {"request": request})

@router.post("/diary", response_class=HTMLResponse)
def diary_submit(request: Request, summary: str = Form(...), content: str = Form(...), db: Session = Depends(get_db)):
    sentiment = analyze_sentiment(content)
    recommendations = recommendation_map.get(sentiment, recommendation_map["neutral"])
    save_diary(db, summary, content, sentiment, recommendations)
    return RedirectResponse(url="/diary/list", status_code=303)

@router.get("/diary/list", response_class=HTMLResponse)
def diary_list(request: Request, db: Session = Depends(get_db)):
    diaries = get_all_diaries(db)
    result = []
    for diary in diaries:
        result.append({
            "id": diary.id,
            "date": diary.date,
            "summary": diary.summary,
            "recommended_projects": diary.recommended_projects
        })
    return templates.TemplateResponse("diary/diary-list.html", {"request": request, "diaries": result})

@router.get("/diary/{diary_id}", response_class=HTMLResponse)
def diary_detail(diary_id: int, request: Request, db: Session = Depends(get_db)):
    diary = db.query(Diary).filter(Diary.id == diary_id).first()
    if not diary:
        return templates.TemplateResponse("diary/diary-result.html", {"request": request, "error": "존재하지 않는 일기입니다."})
    import json
    recommended_projects = json.loads(diary.recommended_projects or '[]')
    return templates.TemplateResponse("diary/diary-result.html", {
        "request": request,
        "diary": {
            "id": diary.id,
            "date": diary.date,
            "summary": diary.summary,
            "content": diary.content,
            "sentiment": diary.sentiment,
            "recommended_projects": recommended_projects
        }
    })