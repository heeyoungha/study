import logging
import traceback
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from routes import diary, bookclub, admin
import os
from starlette.exceptions import HTTPException as StarletteHTTPException

# logs 디렉토리 생성
os.makedirs("logs", exist_ok=True)

# 루트 로거 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler("logs/app.log"),
        logging.StreamHandler()
    ]
)

# uvicorn.error 로거에도 파일 핸들러 추가
uvicorn_logger = logging.getLogger("uvicorn.error")
if not any(isinstance(h, logging.FileHandler) for h in uvicorn_logger.handlers):
    uvicorn_logger.addHandler(logging.FileHandler("logs/app.log"))

app = FastAPI(title="Diary Sentiment & Project Recommendation API",
              description="일기 감정 분석 및 프로젝트 추천 서비스",
              version="1.0.0")

# Static 파일 설정
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

app.include_router(diary.router)
app.include_router(bookclub.router)
app.include_router(admin.router)

@app.exception_handler(Exception)
async def all_exception_handler(request: Request, exc: Exception):
    tb = ''.join(traceback.format_exception(type(exc), exc, exc.__traceback__))
    logging.error(f"500 ERROR: {request.url} - {exc}\n{tb}")
    return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})

@app.get("/")
async def read_root():
    return RedirectResponse(url="/docs")

@app.get("/python/swagger")
async def swagger_redirect():
    return RedirectResponse(url="/docs")

@app.get("/python/api-docs")
async def api_docs_redirect():
    return RedirectResponse(url="/docs")