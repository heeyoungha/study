from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Diary Sentiment & Project Recommendation API",
              description="일기 감정 분석 및 프로젝트 추천 서비스",
              version="1.0.0")

class DiaryRequest(BaseModel):
    text: str

class DiaryResponse(BaseModel):
    sentiment: str
    recommendations: List[str]

# 간단한 감정 단어 리스트
positive_words = ["좋다", "행복", "기쁘다", "즐겁다", "신난다", "감사", "사랑", "설레"]
negative_words = ["힘들다", "슬프다", "우울", "짜증", "화난다", "지치다", "외롭다", "불안"]

# 감정별 추천 프로젝트
recommendation_map = {
    "positive": ["리더십 프로젝트", "자원봉사 챌린지", "창의적 글쓰기 모임"],
    "negative": ["힐링 독서 프로젝트", "마음챙김 명상 챌린지", "산책 모임"],
    "neutral": ["기술 스터디 그룹", "운동 습관 만들기", "취미 탐색 프로젝트"]
}

def analyze_sentiment(text: str) -> str:
    if any(word in text for word in positive_words):
        return "positive"
    if any(word in text for word in negative_words):
        return "negative"
    return "neutral"

@app.post("/diary", response_model=DiaryResponse)
def write_diary(req: DiaryRequest):
    sentiment = analyze_sentiment(req.text)
    recommendations = recommendation_map.get(sentiment, recommendation_map["neutral"])
    return DiaryResponse(sentiment=sentiment, recommendations=recommendations)

# 기존 예시 엔드포인트 유지
@app.get("/")
def read_root():
    return {"Hello": "World"} 