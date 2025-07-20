from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from routes import diary, bookclub


app = FastAPI(title="Diary Sentiment & Project Recommendation API",
              description="일기 감정 분석 및 프로젝트 추천 서비스",
              version="1.0.0")

templates = Jinja2Templates(directory="templates")

app.include_router(diary.router)
app.include_router(bookclub.router)

@app.get("/")
async def read_root():
    return RedirectResponse(url="/docs")

@app.get("/swagger")
async def swagger_redirect():
    return RedirectResponse(url="/docs")

@app.get("/api-docs")
async def api_docs_redirect():
    return RedirectResponse(url="/docs") 