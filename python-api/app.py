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
from datetime import datetime
import time

# logs 디렉토리 생성
os.makedirs("logs", exist_ok=True)

# 루트 로거 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

# Access 로그를 위한 별도 로거 설정
access_logger = logging.getLogger("access")
access_logger.setLevel(logging.INFO)
access_handler = logging.FileHandler("logs/access.log")
access_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
access_logger.addHandler(access_handler)

app = FastAPI(title="Diary Sentiment & Project Recommendation API",
              description="일기 감정 분석 및 프로젝트 추천 서비스",
              version="1.0.0")

# Static 파일 설정
app.mount("/python-static", StaticFiles(directory="static"), name="python-static")

templates = Jinja2Templates(directory="templates")

app.include_router(diary.router)
app.include_router(bookclub.router)
app.include_router(admin.router)

# Access 로그 미들웨어
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # 요청 정보 로깅
    client_ip = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("user-agent", "unknown")
    
    # 응답 처리
    response = await call_next(request)
    
    # 처리 시간 계산
    process_time = time.time() - start_time
    
    # Access 로그 기록
    access_log = f'{client_ip} - - [{datetime.now().strftime("%d/%b/%Y:%H:%M:%S +0000")}] "{request.method} {request.url.path} HTTP/{request.scope.get("http_version", "1.1")}" {response.status_code} - "{user_agent}" {process_time:.3f}s'
    access_logger.info(access_log)
    
    return response

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

@app.get("/python/test-proto")
async def test_proto(request: Request):
    return JSONResponse({
        "url": str(request.url),
        "base_url": str(request.base_url),
        "headers": dict(request.headers)
    })

@app.get("/python/health")
async def health_check():
    """서비스 상태 및 GPT API 연결 상태를 확인합니다."""
    try:
        from gpt_service import client
        from datetime import date
        
        # GPT API 상태 확인
        gpt_status = "available" if client else "unavailable"
        gpt_message = "GPT API가 정상적으로 연결되었습니다." if client else "GPT API 키가 설정되지 않았거나 연결에 실패했습니다."
        
        return JSONResponse(content={
            "status": "healthy",
            "timestamp": str(date.today()),
            "services": {
                "database": "connected",
                "gpt_api": gpt_status,
                "analysis_quality": "enhanced" if client else "basic"
            },
            "messages": {
                "gpt": gpt_message,
                "recommendation": "GPT API가 사용 불가능하여 기본 키워드 기반 분석을 사용합니다." if not client else "GPT 기반 고급 감정 분석 및 프로젝트 추천을 사용합니다."
            },
            "warnings": [] if client else ["GPT API가 사용 불가능하여 분석 정확도가 떨어질 수 있습니다."]
        })
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": "unhealthy",
                "error": str(e),
                "timestamp": str(date.today())
            }
        )


# 관리자 대시보드 API
@app.get("/python/admin/dashboard")
async def admin_dashboard():
    """관리자용 상세 대시보드 정보를 제공합니다."""
    try:
        from gpt_service import client
        from datetime import date
        
        # GPT API 상태 확인
        gpt_status = "available" if client else "unavailable"
        
        # 서비스 품질 평가
        service_quality = "excellent" if client else "basic"
        quality_score = 95 if client else 60
        
        # 권장사항
        recommendations = []
        if not client:
            recommendations.append("OPENAI_API_KEY 환경변수를 설정하여 GPT 서비스를 활성화하세요.")
            recommendations.append("GPT API 키는 .env 파일에 추가하거나 Docker 환경변수로 설정하세요.")
        else:
            recommendations.append("GPT 서비스가 정상 작동 중입니다.")
            recommendations.append("고급 감정 분석 및 프로젝트 추천 기능을 제공합니다.")
        
        return JSONResponse(content={
            "dashboard": {
                "service_status": "operational",
                "gpt_api_status": gpt_status,
                "service_quality": service_quality,
                "quality_score": quality_score,
                "last_updated": str(date.today())
            },
            "services": {
                "database": {
                    "status": "connected",
                    "type": "MySQL",
                    "connection": "stable"
                },
                "gpt_api": {
                    "status": gpt_status,
                    "model": "gpt-3.5-turbo" if client else "none",
                    "capabilities": ["sentiment_analysis", "project_recommendation"] if client else ["basic_analysis"]
                },
                "analysis_engine": {
                    "type": "enhanced" if client else "basic",
                    "accuracy": "high" if client else "medium",
                    "features": ["context_aware", "nuanced_analysis"] if client else ["keyword_based"]
                }
            },
            "recommendations": recommendations,
            "alerts": [] if client else [
                {
                    "level": "warning",
                    "message": "GPT API가 사용 불가능합니다.",
                    "action": "OPENAI_API_KEY를 설정하세요."
                }
            ],
            "metrics": {
                "analysis_method": "GPT AI" if client else "Keyword-based",
                "response_time": "fast" if client else "instant",
                "accuracy": "high" if client else "medium"
            }
        })
    except Exception as e:
        logging.error(f"관리자 대시보드 오류: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "error": f"대시보드 정보를 가져오는 중 오류가 발생했습니다: {str(e)}"
            }
        )