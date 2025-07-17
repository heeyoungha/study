from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from routes import diary


app = FastAPI(title="Diary Sentiment & Project Recommendation API",
              description="일기 감정 분석 및 프로젝트 추천 서비스",
              version="1.0.0")

templates = Jinja2Templates(directory="templates")

app.include_router(diary.router)

@app.get("/")
def read_root():
    return {"Hello": "World"} 