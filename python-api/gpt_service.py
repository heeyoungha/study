import os
import json
import asyncio
import logging
from dotenv import load_dotenv

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# .env 파일 로드
load_dotenv()

# OpenAI API 키 설정
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# OpenAI 클라이언트 초기화 (API 키가 있을 때만)
client = None
if OPENAI_API_KEY:
    try:
        from openai import AsyncOpenAI
        client = AsyncOpenAI(api_key=OPENAI_API_KEY)
        logger.info("✅ GPT API 클라이언트가 성공적으로 초기화되었습니다.")
        logger.info("🚀 고급 감정 분석 및 프로젝트 추천 기능이 활성화되었습니다.")
    except Exception as e:
        logger.error(f"❌ GPT API 클라이언트 초기화 실패: {e}")
        client = None
else:
    logger.warning("⚠️ OPENAI_API_KEY가 설정되지 않았습니다.")
    logger.warning("⚠️ 기본 키워드 기반 감정 분석을 사용합니다.")
    logger.warning("⚠️ 분석 정확도가 떨어질 수 있습니다.")

# 감정 분석을 위한 프롬프트
SENTIMENT_ANALYSIS_PROMPT = """
다음 일기 텍스트의 감정을 분석하여 다음 중 하나로 분류해주세요:
- positive (긍정적): 기쁨, 행복, 만족, 감사, 희망, 설렘, 성취감 등
- negative (부정적): 슬픔, 우울, 분노, 불안, 스트레스, 실망, 외로움 등  
- neutral (중립적): 평온, 일상, 객관적, 무관심 등

분석할 텍스트: {text}

응답은 반드시 다음 JSON 형식으로만 해주세요:
{{"sentiment": "positive|negative|neutral", "confidence": 0.95, "reason": "분석 이유"}}
"""

# 프로젝트 추천을 위한 프롬프트
PROJECT_RECOMMENDATION_PROMPT = """
다음 일기 내용을 바탕으로 사용자에게 도움이 될 만한 프로젝트나 활동을 추천해주세요.

일기 내용: {text}
감정: {sentiment}

다음 카테고리 중에서 추천해주세요:
- 자기계발: 학습, 스킬 개발, 취미 활동
- 사회활동: 봉사, 모임, 네트워킹
- 건강관리: 운동, 명상, 휴식
- 창작활동: 글쓰기, 예술, 공예
- 기술활동: 프로그래밍, 디자인, 개발

응답은 반드시 다음 JSON 형식으로만 해주세요:
{{"projects": ["프로젝트1", "프로젝트2", "프로젝트3"], "reason": "추천 이유"}}
"""

async def analyze_sentiment_with_gpt(text: str) -> dict:
    """
    GPT를 사용하여 텍스트의 감정을 분석합니다.
    
    Args:
        text (str): 분석할 텍스트
        
    Returns:
        dict: {"sentiment": "positive|negative|neutral", "confidence": float, "reason": str}
    """
    # GPT API가 사용 불가능한 경우 기본 분석 사용
    if not client:
        logger.warning(f"⚠️ GPT API 사용 불가능 - 기본 키워드 분석 사용: {text[:50]}...")
        return fallback_sentiment_analysis(text)
    
    try:
        logger.info(f"🤖 GPT API를 사용한 감정 분석 시작: {text[:50]}...")
        
        # GPT API 호출
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "당신은 감정 분석 전문가입니다. 주어진 텍스트의 감정을 정확히 분석해주세요."
                },
                {
                    "role": "user", 
                    "content": SENTIMENT_ANALYSIS_PROMPT.format(text=text)
                }
            ],
            temperature=0.3,
            max_tokens=200
        )
        
        # 응답 파싱
        content = response.choices[0].message.content.strip()
        
        # JSON 파싱 시도
        try:
            result = json.loads(content)
            logger.info(f"✅ GPT 감정 분석 완료: {result.get('sentiment')} (신뢰도: {result.get('confidence')})")
            return {
                "sentiment": result.get("sentiment", "neutral"),
                "confidence": result.get("confidence", 0.5),
                "reason": result.get("reason", "GPT 분석 결과")
            }
        except json.JSONDecodeError:
            # JSON 파싱 실패 시 텍스트에서 감정 추출
            logger.warning(f"⚠️ GPT 응답 JSON 파싱 실패, 텍스트 기반 추출: {content}")
            sentiment = "neutral"
            if "positive" in content.lower():
                sentiment = "positive"
            elif "negative" in content.lower():
                sentiment = "negative"
            
            return {
                "sentiment": sentiment,
                "confidence": 0.7,
                "reason": "GPT 분석 결과 (JSON 파싱 실패)"
            }
            
    except Exception as e:
        logger.error(f"❌ GPT API 호출 중 오류: {e}")
        logger.warning(f"⚠️ 기본 감정 분석으로 대체: {text[:50]}...")
        # 오류 발생 시 기본 감정 분석 사용
        return fallback_sentiment_analysis(text)

async def recommend_projects_with_gpt(text: str, sentiment: str) -> dict:
    """
    GPT를 사용하여 감정에 맞는 프로젝트를 추천합니다.
    
    Args:
        text (str): 일기 텍스트
        sentiment (str): 감정 분석 결과
        
    Returns:
        dict: {"projects": [list], "reason": str}
    """
    # GPT API가 사용 불가능한 경우 기본 추천 사용
    if not client:
        logger.warning(f"⚠️ GPT API 사용 불가능 - 기본 프로젝트 추천 사용 (감정: {sentiment})")
        return fallback_project_recommendation(sentiment)
    
    try:
        logger.info(f"🤖 GPT API를 사용한 프로젝트 추천 시작 (감정: {sentiment})")
        
        # GPT API 호출
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "당신은 개인 성장과 자기계발 전문가입니다. 사용자의 상황에 맞는 프로젝트를 추천해주세요."
                },
                {
                    "role": "user",
                    "content": PROJECT_RECOMMENDATION_PROMPT.format(text=text, sentiment=sentiment)
                }
            ],
            temperature=0.7,
            max_tokens=300
        )
        
        # 응답 파싱
        content = response.choices[0].message.content.strip()
        
        try:
            result = json.loads(content)
            projects = result.get("projects", [])
            logger.info(f"✅ GPT 프로젝트 추천 완료: {len(projects)}개 프로젝트 추천")
            return {
                "projects": projects,
                "reason": result.get("reason", "GPT 추천 결과")
            }
        except json.JSONDecodeError:
            # JSON 파싱 실패 시 기본 추천 사용
            logger.warning(f"⚠️ GPT 응답 JSON 파싱 실패, 기본 추천 사용: {content}")
            return fallback_project_recommendation(sentiment)
            
    except Exception as e:
        logger.error(f"❌ GPT 프로젝트 추천 중 오류: {e}")
        logger.warning(f"⚠️ 기본 프로젝트 추천으로 대체 (감정: {sentiment})")
        return fallback_project_recommendation(sentiment)

def fallback_sentiment_analysis(text: str) -> dict:
    """
    GPT API 실패 시 사용할 기본 감정 분석
    """
    logger.info(f"🔍 기본 키워드 기반 감정 분석: {text[:50]}...")
    
    positive_words = ["좋다", "행복", "기쁘다", "즐겁다", "신난다", "감사", "사랑", "설레", "만족", "성취"]
    negative_words = ["힘들다", "슬프다", "우울", "짜증", "화난다", "지치다", "외롭다", "불안", "스트레스", "실망"]
    
    text_lower = text.lower()
    
    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)
    
    if positive_count > negative_count:
        sentiment = "positive"
        confidence = min(0.9, 0.5 + positive_count * 0.1)
    elif negative_count > positive_count:
        sentiment = "negative"
        confidence = min(0.9, 0.5 + negative_count * 0.1)
    else:
        sentiment = "neutral"
        confidence = 0.5
    
    logger.info(f"📊 기본 분석 결과: {sentiment} (신뢰도: {confidence:.2f})")
    
    return {
        "sentiment": sentiment,
        "confidence": confidence,
        "reason": "기본 키워드 기반 분석"
    }

def fallback_project_recommendation(sentiment: str) -> dict:
    """
    GPT API 실패 시 사용할 기본 프로젝트 추천
    """
    logger.info(f"📋 기본 프로젝트 추천 (감정: {sentiment})")
    
    recommendation_map = {
        "positive": [
            "리더십 프로젝트", 
            "자원봉사 챌린지", 
            "창의적 글쓰기 모임",
            "멘토링 프로그램",
            "커뮤니티 활동"
        ],
        "negative": [
            "힐링 독서 프로젝트", 
            "마음챙김 명상 챌린지", 
            "산책 모임",
            "예술 치료 활동",
            "자기 돌봄 프로젝트"
        ],
        "neutral": [
            "기술 스터디 그룹", 
            "운동 습관 만들기", 
            "취미 탐색 프로젝트",
            "일상 기록 프로젝트",
            "새로운 경험 도전"
        ]
    }
    
    projects = recommendation_map.get(sentiment, recommendation_map["neutral"])
    logger.info(f"📋 기본 추천 완료: {len(projects)}개 프로젝트")
    
    return {
        "projects": projects,
        "reason": f"기본 {sentiment} 감정 기반 추천"
    }

# 기존 함수들과의 호환성을 위한 래퍼 함수들
async def analyze_sentiment_async(text: str) -> str:
    """
    비동기 감정 분석 (기존 함수와 호환)
    """
    result = await analyze_sentiment_with_gpt(text)
    return result["sentiment"]

async def recommend_projects_async(text: str, sentiment: str) -> list:
    """
    비동기 프로젝트 추천 (기존 함수와 호환)
    """
    result = await recommend_projects_with_gpt(text, sentiment)
    return result["projects"] 