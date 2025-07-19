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
from database import SessionLocal
from sqlalchemy.orm import Session
from datetime import date

def analyze_sentiment(content: str) -> str:
    if any(word in content for word in positive_words):
        return "positive"
    if any(word in content for word in negative_words):
        return "negative"
    return "neutral"

def save_diary(db: Session, summary: str, content: str, sentiment: str, recommended_projects: list = None):
    import json
    diary = Diary(
        summary=summary,
        content=content, 
        sentiment=sentiment,
        date=date.today(),
        recommended_projects=json.dumps(recommended_projects or [])
    )
    db.add(diary)
    db.commit()
    db.refresh(diary)
    return diary

def get_all_diaries(db: Session):
    diaries = db.query(Diary).order_by(Diary.date.desc()).all()
    import json
    for diary in diaries:
        diary.recommended_projects = json.loads(diary.recommended_projects or '[]')
    return diaries

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