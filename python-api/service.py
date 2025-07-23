# 감정 단어 리스트 및 추천 맵, 분석 함수 분리

positive_words = ["좋다", "행복", "기쁘다", "즐겁다", "신난다", "감사", "사랑", "설레"]
negative_words = ["힘들다", "슬프다", "우울", "짜증", "화난다", "지치다", "외롭다", "불안"]

recommendation_map = {
    "positive": ["리더십 프로젝트", "자원봉사 챌린지", "창의적 글쓰기 모임"],
    "negative": ["힐링 독서 프로젝트", "마음챙김 명상 챌린지", "산책 모임"],
    "neutral": ["기술 스터디 그룹", "운동 습관 만들기", "취미 탐색 프로젝트"]
}

import json
from models import Diary
from database import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import date
import asyncio
from gpt_service import analyze_sentiment_async, recommend_projects_async, analyze_sentiment_with_gpt, recommend_projects_with_gpt

# 기존 동기 감정 분석 (fallback용)
def analyze_sentiment(content: str) -> str:
    if any(word in content for word in positive_words):
        return "positive"
    if any(word in content for word in negative_words):
        return "negative"
    return "neutral"

# 새로운 비동기 감정 분석 (GPT 사용)
async def analyze_sentiment_enhanced(content: str) -> dict:
    """
    GPT를 사용한 향상된 감정 분석
    """
    return await analyze_sentiment_with_gpt(content)

async def save_diary_async(db: AsyncSession, summary: str, content: str, sentiment: str, recommended_projects: list = None, user_id: int = None):
    import json
    diary = Diary(
        summary=summary,
        content=content, 
        sentiment=sentiment,
        date=date.today(),
        recommended_projects=json.dumps(recommended_projects or []),
        user_id=user_id
    )
    db.add(diary)
    await db.commit()
    await db.refresh(diary)
    return diary

async def get_all_diaries_async(db: AsyncSession):
    from models import User
    from sqlalchemy.orm import selectinload
    
    # User 테이블과 조인하여 작성자 정보도 함께 가져오기 (is_deleted = false 조건 추가)
    result = await db.execute(
        select(Diary, User.username)
        .outerjoin(User, (Diary.user_id == User.id) & (User.is_deleted == False))
        .order_by(Diary.date.desc())
    )
    
    # 결과를 튜플로 받아서 처리
    diary_user_tuples = result.all()
    diaries = []
    for i, (diary, username) in enumerate(diary_user_tuples):

        # recommended_projects를 JSON에서 파싱
        import json
        diary.recommended_projects = json.loads(diary.recommended_projects or '[]')
        # username 속성 추가
        diary.username = username or "알 수 없음"
        diaries.append(diary)

    return diaries

# 새로운 비동기 프로젝트 추천 (GPT 사용)
async def recommend_projects_enhanced(content: str, sentiment: str) -> dict:
    """
    GPT를 사용한 향상된 프로젝트 추천
    """
    return await recommend_projects_with_gpt(content, sentiment)

def recommend_projects_from_diary(content: str) -> list:
    if "감동" in content or "영감" in content:
        return ["감상문 공유 프로젝트", "책 속 명언 모음"]
    elif "어려움" in content or "이해 안됨" in content:
        return ["스터디 그룹 결성", "작가 인터뷰 찾아보기"]
    else:
        return ["서평 블로그 작성", "독서 토론회 개최"]

def recommend_projects_from_review(review: str) -> list:
    if "감동" in review or "영감" in review:
        return ["감상문 공유 프로젝트", "책 속 명언 모음"]
    elif "어려움" in review or "이해 안됨" in review:
        return ["스터디 그룹 결성", "작가 인터뷰 찾아보기"]
    else:
        return ["서평 블로그 작성", "독서 토론회 개최"] 