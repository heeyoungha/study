from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal
from models import BookClubEntry
from schemas import BookClubEntryCreate, BookClubEntryResponse
from service import recommend_projects_from_review
import json
import os
from datetime import date

router = APIRouter()

templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), '../templates'))

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def save_bookclub_entry(db, book_title, review, summary, entry_date):
    recommended_projects = recommend_projects_from_review(review)
    db_entry = BookClubEntry(
        date=entry_date,
        book_title=book_title,
        review=review,
        summary=summary,
        recommended_projects=json.dumps(recommended_projects)
    )
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry, recommended_projects

# JSON API용
@router.post("/bookclub/", response_model=BookClubEntryResponse)
def create_bookclub_entry_api(entry: BookClubEntryCreate, db: Session = Depends(get_db)):
    db_entry, recommended_projects = save_bookclub_entry(db, entry.book_title, entry.review, entry.summary, entry.date)
    return BookClubEntryResponse(
        id=db_entry.id,
        date=db_entry.date,
        book_title=db_entry.book_title,
        review=db_entry.review,
        summary=db_entry.summary,
        recommended_projects=recommended_projects
    )

# HTML Form 전송용
@router.post("/bookclub/form")
def create_bookclub_entry_form(
    book_title: str = Form(...),
    review: str = Form(...),
    summary: str = Form(...),
    db: Session = Depends(get_db)
):
    entry_date = date.today()
    save_bookclub_entry(db, book_title, review, summary, entry_date)
    return RedirectResponse(url="/bookclub/list", status_code=303)

@router.get("/bookclub")
def bookclub_form(request: Request):
    return templates.TemplateResponse("bookclub-form.html", {"request": request})

@router.get("/bookclub/list")
def bookclub_list(request: Request, db: Session = Depends(get_db)):
    entries = db.query(BookClubEntry).order_by(BookClubEntry.date.desc()).all()
    result = []
    for entry in entries:
        recommended_projects = json.loads(entry.recommended_projects or '[]')
        result.append({
            "id": entry.id,
            "date": entry.date,
            "book_title": entry.book_title,
            "review": entry.review,
            "summary": entry.summary,
            "recommended_projects": recommended_projects
        })
    return templates.TemplateResponse("bookclub-list.html", {"request": request, "entries": result})

@router.get("/bookclub/", response_model=List[BookClubEntryResponse])
def get_bookclub_entries(db: Session = Depends(get_db)):
    entries = db.query(BookClubEntry).order_by(BookClubEntry.date.desc()).all()
    result = []
    for entry in entries:
        recommended_projects = json.loads(entry.recommended_projects or '[]')
        result.append(BookClubEntryResponse(
            id=entry.id,
            date=entry.date,
            book_title=entry.book_title,
            review=entry.review,
            recommended_projects=recommended_projects
        ))
    return result

@router.get("/bookclub/{entry_id}")
def bookclub_detail(entry_id: int, request: Request, db: Session = Depends(get_db)):
    entry = db.query(BookClubEntry).filter(BookClubEntry.id == entry_id).first()
    if not entry:
        return templates.TemplateResponse("bookclub-result.html", {"request": request, "error": "존재하지 않는 독후감입니다."})
    import json
    recommended_projects = json.loads(entry.recommended_projects or '[]')
    return templates.TemplateResponse("bookclub-result.html", {
        "request": request,
        "entry": {
            "id": entry.id,
            "date": entry.date,
            "book_title": entry.book_title,
            "review": entry.review,
            "summary": entry.summary,
            "recommended_projects": recommended_projects
        }
    }) 