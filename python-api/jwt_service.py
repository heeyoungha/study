import os
import jwt
import logging
from fastapi import Depends
from fastapi import Cookie
from typing import Optional, Dict

logger = logging.getLogger(__name__)

# Spring Boot와 동일한 환경변수 사용
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default-jwt-secret")
JWT_ALGORITHM = "HS256"  # Spring Boot와 동일한 알고리즘 사용

def get_user_info_from_jwt(token: str):
    try:
        # Spring Boot와 동일한 시크릿 키와 알고리즘 사용
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return {
            "user_id": int(payload.get("sub")),
            "username": payload.get("username"),
            "email": payload.get("email"),
            "role": payload.get("role"),
        }
    except Exception as e:
        logger.error(f"[ERROR] get_user_info_from_jwt 디코딩 실패: {e}")
        return None
        
async def get_current_user(jwt: str = Cookie(None)) -> Optional[Dict]:
    """JWT에서 현재 사용자 정보를 추출하는 의존성"""
    if not jwt:
        logger.warning("[DEBUG] JWT 쿠키가 없습니다.")
        return None
    
    user_info = get_user_info_from_jwt(jwt)
    if not user_info or 'user_id' not in user_info:
        logger.warning("[DEBUG] JWT에서 user_id를 추출할 수 없습니다.")
        return None
    
    return user_info

async def get_current_user_id(current_user: Optional[Dict] = Depends(get_current_user)) -> Optional[int]:
    """현재 사용자 ID만 추출하는 의존성"""
    return current_user['user_id'] if current_user else None