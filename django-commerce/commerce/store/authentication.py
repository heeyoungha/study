"""
Django Commerce JWT 인증 모듈

Spring Boot에서 생성한 JWT 토큰을 검증하여 Django Commerce에서 사용자 인증을 처리합니다.
"""

import jwt
import os
from django.contrib.auth.models import User, AnonymousUser
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings

class JWTAuthentication(BaseAuthentication):
    """
    Spring Boot JWT 토큰을 검증하는 커스텀 인증 클래스
    """
    
    def authenticate(self, request):
        # Authorization 헤더에서 토큰 추출
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header:
            # 쿠키에서 JWT 토큰 확인 (Spring Boot에서 설정한 쿠키)
            jwt_cookie = request.COOKIES.get('jwt')
            if not jwt_cookie:
                return None
            token = jwt_cookie
        else:
            # Bearer 토큰 형식 확인
            if not auth_header.startswith('Bearer '):
                return None
            token = auth_header.split(' ')[1]
        
        try:
            # JWT 토큰 검증 (Spring Boot와 동일한 시크릿 키 사용)
            secret_key = os.getenv('JWT_SECRET_KEY', settings.SECRET_KEY)
            payload = jwt.decode(token, secret_key, algorithms=['HS512'])
            
            # 사용자 정보 추출 (Spring Boot JWT 구조에 맞춤)
            user_id = payload.get('sub')  # subject에 user_id가 저장됨
            username = payload.get('username')
            email = payload.get('email')
            
            if not user_id or not username:
                raise AuthenticationFailed('Invalid token payload')
            
            # Django 사용자 조회 또는 생성
            user = self.get_or_create_user(user_id, username, email)
            
            return (user, token)
            
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')
        except Exception as e:
            raise AuthenticationFailed(f'Authentication failed: {str(e)}')
    
    def get_or_create_user(self, user_id, username, email):
        """
        JWT에서 추출한 사용자 정보로 Django 사용자를 조회하거나 생성
        """
        try:
            # user_id로 기존 사용자 조회 (가장 정확한 방법)
            user = User.objects.get(id=user_id)
            # 사용자 정보 업데이트 (필요시)
            if user.username != username or user.email != email:
                user.username = username
                user.email = email
                user.save()
            return user
        except User.DoesNotExist:
            # 새 사용자 생성 (user_id를 Django User의 ID로 사용)
            user = User.objects.create_user(
                id=user_id,  # Spring Boot의 user_id를 Django User ID로 사용
                username=username,
                email=email,
                password=None  # OAuth 사용자는 비밀번호 없음
            )
            return user
    
    def authenticate_header(self, request):
        return 'Bearer realm="api"'

class JWTMiddleware:
    """
    JWT 토큰을 미들웨어에서 처리하여 request.user를 설정
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # JWT 토큰 검증
        auth = JWTAuthentication()
        try:
            user, token = auth.authenticate(request)
            request.user = user
            request.jwt_token = token
        except:
            request.user = AnonymousUser()
        
        response = self.get_response(request)
        return response 