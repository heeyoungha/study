from fastapi import APIRouter, Depends, HTTPException, Request, Form, Cookie
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, join
from typing import List
from database import get_async_db
from models import BookClubEntry, User
from schemas import BookClubEntryCreate, BookClubEntryResponse
from service import recommend_projects_enhanced
from gpt_service import recommend_projects_with_gpt
from jwt_service import get_user_info_from_jwt
from fastapi import Depends
import json
import os
from datetime import date
import jwt
import logging
from typing import Optional
from jwt_service import get_current_user_id

logger = logging.getLogger(__name__)

router = APIRouter()

templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), '../templates'))

async def save_bookclub_entry_async(db: AsyncSession, book_title: str, review: str, summary: str, entry_date: date, user_id: int = None):
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"[DEBUG] save_bookclub_entry_async 호출됨 - user_id: {user_id}")
    
    # GPT를 사용한 향상된 프로젝트 추천
    recommendation_result = await recommend_projects_with_gpt(review, "neutral")  # 독후감은 중립적으로 처리
    recommended_projects = recommendation_result["projects"]
    
    db_entry = BookClubEntry(
        date=entry_date,
        book_title=book_title,
        review=review,
        summary=summary,
        recommended_projects=json.dumps(recommended_projects),
        user_id=user_id
    )
    
    logger.info(f"[DEBUG] BookClubEntry 객체 생성됨 - user_id: {db_entry.user_id}")
    
    db.add(db_entry)
    await db.commit()
    await db.refresh(db_entry)
    
    logger.info(f"[DEBUG] 독서모임 저장 완료 - ID: {db_entry.id}, user_id: {db_entry.user_id}")
    return db_entry, recommended_projects

# JSON API용
@router.post("/bookclub/", response_model=BookClubEntryResponse)
async def create_bookclub_entry_api(
    entry: BookClubEntryCreate, 
    db: AsyncSession = Depends(get_async_db), 
    user_id: Optional[int] = Depends(get_current_user_id)
):
    db_entry, recommended_projects = await save_bookclub_entry_async(db, entry.book_title, entry.review, entry.summary, entry.date, user_id=user_id)
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
async def create_bookclub_entry_form(
    book_title: str = Form(...),
    review: str = Form(...),
    summary: str = Form(...),
    db: AsyncSession = Depends(get_async_db),
    user_id: Optional[int] = Depends(get_current_user_id)
):
    entry_date = date.today()
    await save_bookclub_entry_async(db, book_title, review, summary, entry_date, user_id=user_id)
    return RedirectResponse(url="/bookclub/list", status_code=303)

@router.get("/bookclub")
async def bookclub_form(request: Request):
    return templates.TemplateResponse("bookclub-form.html", {"request": request})

@router.get("/bookclub/list")
async def bookclub_list(request: Request, db: AsyncSession = Depends(get_async_db)):
    
    # User 테이블 직접 조회 테스트
    # user_result = await db.execute(select(User).filter(User.id == 1))
    # test_user = user_result.scalar_one_or_none()
    # if test_user:
    #     logger.info(f"[DEBUG] User 테이블 조회 성공 - ID: {test_user.id}, Username: {test_user.username}, Email: {test_user.email}")
    # else:
    #     logger.info("[DEBUG] User 테이블 조회 실패 - user_id=1인 사용자를 찾을 수 없음")
    
    # is_deleted = false 조건 추가
    stmt = select(BookClubEntry, User.username).join(
        User, 
        (BookClubEntry.user_id == User.id) & (User.is_deleted == False), 
        isouter=True
    ).order_by(BookClubEntry.date.desc())
    
    result = await db.execute(stmt)
    entries = result.all()
    
    out = []
    for i, (entry, username) in enumerate(entries):
        
        recommended_projects = entry.recommended_projects
        if isinstance(recommended_projects, str):
            recommended_projects = json.loads(recommended_projects or "[]")
        
        entry_data = {
            "id": entry.id,
            "date": entry.date,
            "book_title": entry.book_title,
            "review": entry.review,
            "summary": entry.summary,
            "recommended_projects": recommended_projects,
            "username": username or "(알수없음)"
        }
        out.append(entry_data)

    return templates.TemplateResponse("bookclub-list.html", {"request": request, "entries": out})

@router.get("/bookclub/", response_model=List[BookClubEntryResponse])
async def get_bookclub_entries(db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(BookClubEntry).order_by(BookClubEntry.date.desc()))
    entries = result.scalars().all()
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
async def bookclub_detail(entry_id: int, request: Request, db: AsyncSession = Depends(get_async_db)):
    # is_deleted = false 조건 추가
    stmt = select(BookClubEntry, User.username).join(
        User, 
        (BookClubEntry.user_id == User.id) & (User.is_deleted == False), 
        isouter=True
    ).filter(BookClubEntry.id == entry_id)
    
    result = await db.execute(stmt)
    row = result.first()
    if not row:
        return templates.TemplateResponse("bookclub-result.html", {"request": request, "error": "존재하지 않는 독후감입니다."})
    entry, username = row
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
            "recommended_projects": recommended_projects,
            "username": username or "(알수없음)"
        }
    }) 