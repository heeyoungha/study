from fastapi import APIRouter, Depends, Request, Form, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from service import analyze_sentiment_enhanced, recommend_projects_enhanced, save_diary_async, get_all_diaries_async
from schemas import DiaryCreate, DiaryRead
from database import get_async_db
from models import Diary
from datetime import date
from sqlalchemy import select
from fastapi import Depends
import os
from gpt_service import client
import logging
import json
from jwt_service import get_user_info_from_jwt
from typing import Optional
from jwt_service import get_current_user_id

logger = logging.getLogger(__name__)

templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), '../templates'))

router = APIRouter()

@router.get("/diary", response_class=HTMLResponse)
async def diary_form(request: Request):
    return templates.TemplateResponse("diary/diary-form.html", {"request": request})

@router.post("/diary", response_class=HTMLResponse)
async def diary_submit(
    request: Request, 
    summary: str = Form(...), 
    content: str = Form(...), 
    db: AsyncSession = Depends(get_async_db),
    user_id: Optional[int] = Depends(get_current_user_id)
):
    # GPT를 사용한 향상된 감정 분석
    sentiment_result = await analyze_sentiment_enhanced(content)
    sentiment = sentiment_result["sentiment"]
    
    # GPT를 사용한 향상된 프로젝트 추천
    recommendation_result = await recommend_projects_enhanced(content, sentiment)
    recommended_projects = recommendation_result["projects"]
    
    # 일기 저장 시 user_id 전달
    await save_diary_async(db, summary, content, sentiment, recommended_projects, user_id)
    return RedirectResponse(url="/diary/list", status_code=303)

@router.get("/diary/list", response_class=HTMLResponse)
async def diary_list(
    request: Request, 
    db: AsyncSession = Depends(get_async_db),
    current_user_id: Optional[int] = Depends(get_current_user_id)
):

    # 현재 사용자의 일기만 조회 (로그인한 경우) 또는 모든 일기 조회 (비로그인 시)
    # if current_user_id:
    #     diaries = await get_user_diaries_async(db, current_user_id)  # 사용자별 일기 조회 함수 필요
    # else:
    #     diaries = await get_all_diaries_async(db)  # 또는 빈 리스트 반환
    
    diaries = await get_all_diaries_async(db)
    result = []
    for i, diary in enumerate(diaries):
        diary_data = {
            "id": diary.id,
            "date": diary.date,
            "summary": diary.summary,
            "recommended_projects": diary.recommended_projects,
            "user_id": diary.user_id,
            "username": getattr(diary, 'username', '알 수 없음')  # username 속성이 없을 경우 기본값
        }
        result.append(diary_data)
    
    return templates.TemplateResponse("diary/diary-list.html", {"request": request, "diaries": result})

@router.get("/diary/{diary_id}", response_class=HTMLResponse)
async def diary_detail(diary_id: int, request: Request, db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(Diary).filter(Diary.id == diary_id))
    diary = result.scalar_one_or_none()
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

# GPT 감정 분석 테스트 API
@router.post("/diary/sentiment-analysis")
async def analyze_sentiment_api(request: Request):
    try:
        body = await request.json()
        text = body.get("text", "")

        if not text:
            return JSONResponse(
                status_code=400,
                content={"error": "텍스트가 필요합니다."}
            )

        # GPT 감정 분석
        sentiment_result = await analyze_sentiment_enhanced(text)

        # GPT API 상태에 따른 메시지 추가
        gpt_status = "GPT API 사용" if client else "기본 키워드 분석 사용"

        return JSONResponse(content={
            "text": text,
            "sentiment": sentiment_result["sentiment"],
            "confidence": sentiment_result["confidence"],
            "reason": sentiment_result["reason"],
            "analysis_method": gpt_status,
            "quality_warning": "GPT API가 사용 불가능하여 분석 정확도가 떨어질 수 있습니다." if not client else None
        })

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"감정 분석 중 오류가 발생했습니다: {str(e)}"}
        )

# GPT 프로젝트 추천 테스트 API
@router.post("/diary/project-recommendation")
async def recommend_projects_api(request: Request):
    try:
        body = await request.json()
        text = body.get("text", "")
        sentiment = body.get("sentiment", "neutral")

        if not text:
            return JSONResponse(
                status_code=400,
                content={"error": "텍스트가 필요합니다."}
            )

        # GPT 프로젝트 추천
        recommendation_result = await recommend_projects_enhanced(text, sentiment)

        # GPT API 상태에 따른 메시지 추가
        gpt_status = "GPT API 사용" if client else "기본 추천 사용"

        return JSONResponse(content={
            "text": text,
            "sentiment": sentiment,
            "projects": recommendation_result["projects"],
            "reason": recommendation_result["reason"],
            "recommendation_method": gpt_status,
            "quality_warning": "GPT API가 사용 불가능하여 추천 품질이 떨어질 수 있습니다." if not client else None
        })

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"프로젝트 추천 중 오류가 발생했습니다: {str(e)}"}
        )

