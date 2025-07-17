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

def analyze_sentiment(text: str) -> str:
    if any(word in text for word in positive_words):
        return "positive"
    if any(word in text for word in negative_words):
        return "negative"
    return "neutral"

def save_diary(db: Session, text: str, sentiment: str, recommended_projects: list = None):
    import json
    diary = Diary(
        text=text,
        sentiment=sentiment,
        recommended_projects=json.dumps(recommended_projects or [])
    )
    db.add(diary)
    db.commit()
    db.refresh(diary)
    return diary

def get_all_diaries(db: Session):
    diaries = db.query(Diary).order_by(Diary.created_at.desc()).all()
    import json
    for diary in diaries:
        diary.recommended_projects = json.loads(diary.recommended_projects or '[]')
    return diaries 