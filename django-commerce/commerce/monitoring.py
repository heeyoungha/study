"""
Django Commerce 모니터링 모듈

이 모듈은 Django Commerce 서비스의 시스템 상태를 모니터링하고
통합 모니터링 대시보드에 필요한 정보를 제공합니다.

주요 기능:
- 시스템 리소스 모니터링 (CPU, 메모리)
- 데이터베이스 연결 상태 확인
- 캐시 상태 확인
- Django 앱 상태 확인
- 에러 로그 분석
- 프로세스 정보 수집
"""

import psutil
import datetime
import os
import re
from collections import deque
import json
from django.db import connection
from django.core.cache import cache
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response

# =============================================================================
# 전역 변수 설정
# =============================================================================

# 모니터링 히스토리 저장 (최근 30개 데이터 포인트)
HEALTH_HISTORY = deque(maxlen=30)
_last_history_time = None  # 마지막 히스토리 업데이트 시간


# =============================================================================
# 유틸리티 함수들
# =============================================================================

def get_recent_error_blocks(log_path, minutes=30, max_lines=300):
    """
    최근 에러 로그 블록을 가져오는 함수
    
    Args:
        log_path (str): 로그 파일 경로
        minutes (int): 몇 분 전까지의 로그를 가져올지 (기본값: 30분)
        max_lines (int): 최대 읽을 라인 수 (기본값: 300줄)
    
    Returns:
        list: 최근 에러 로그 블록들의 리스트 (최대 10개)
    """
    if not os.path.exists(log_path):
        return []
    
    now = datetime.datetime.now()
    result = []
    # 에러 로그 패턴: "2024-01-01 12:00:00,123 ERROR "
    log_pattern = re.compile(r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}),\d+ (ERROR|CRITICAL) ")
    
    try:
        with open(log_path, 'r') as f:
            # 파일의 마지막 max_lines줄만 읽기
            lines = f.readlines()[-max_lines:]
            block = []  # 현재 에러 블록
            block_time = None  # 현재 블록의 시간
            
            for line in lines:
                m = log_pattern.match(line)
                if m:
                    # 이전 블록이 있고 지정된 시간 내라면 저장
                    if block and block_time and (now - block_time).total_seconds() <= minutes * 60:
                        result.append(''.join(block).strip())
                    
                    # 새 에러 블록 시작
                    block = [line]
                    try:
                        # 로그 시간 파싱
                        block_time = datetime.datetime.strptime(m.group(1), "%Y-%m-%d %H:%M:%S")
                    except Exception:
                        block_time = None
                else:
                    # 에러 블록에 속한 라인 추가
                    if block:
                        block.append(line)
            
            # 마지막 블록도 저장
            if block and block_time and (now - block_time).total_seconds() <= minutes * 60:
                result.append(''.join(block).strip())
    except Exception as e:
        result.append(f"로그 파싱 오류: {str(e)}")
    
    return result[-10:]  # 최근 10개만 반환


def get_top_memory_processes(n=5):
    """
    상위 메모리 사용 프로세스 정보를 가져오는 함수
    
    Args:
        n (int): 가져올 프로세스 개수 (기본값: 5개)
    
    Returns:
        tuple: (프로세스 리스트, 전체 메모리)
    """
    procs = []
    total_mem = psutil.virtual_memory().total
    
    try:
        # 모든 프로세스 순회
        for p in psutil.process_iter(['pid', 'name', 'memory_info']):
            try:
                mem = p.info['memory_info'].rss  # RSS (Resident Set Size)
                percent = (mem / total_mem) * 100 if total_mem else 0
                procs.append({
                    'pid': p.info['pid'],
                    'name': p.info['name'],
                    'memory': mem,  # 바이트 단위
                    'memory_mb': round(mem / (1024 * 1024), 2),  # MB 단위
                    'percent_of_total': round(percent, 2)  # 전체 대비 퍼센트
                })
            except Exception:
                # 프로세스 정보 가져오기 실패 시 건너뛰기
                continue
        
        # 메모리 사용량 기준으로 정렬
        procs.sort(key=lambda x: x['memory'], reverse=True)
    except Exception as e:
        # 전체 프로세스 정보 가져오기 실패 시 에러 정보 반환
        procs.append({
            'name': 'Error getting processes',
            'memory_mb': 0,
            'percent_of_total': 0,
            'error': str(e)
        })
    
    return procs[:n], total_mem


def check_database_connection():
    """
    데이터베이스 연결 상태를 확인하는 함수
    
    Returns:
        tuple: (연결 성공 여부, 상태 메시지)
    """
    try:
        with connection.cursor() as cursor:
            # 간단한 쿼리로 연결 테스트
            cursor.execute("SELECT 1")
            cursor.fetchone()
        return True, "정상"
    except Exception as e:
        return False, f"연결 오류: {str(e)}"


def check_cache_status():
    """
    캐시 상태를 확인하는 함수
    
    Returns:
        tuple: (캐시 동작 여부, 상태 메시지)
    """
    try:
        # 테스트 키로 캐시 읽기/쓰기 테스트
        test_key = "health_check_test"
        cache.set(test_key, "test_value", 10)  # 10초 TTL로 설정
        value = cache.get(test_key)
        cache.delete(test_key)  # 테스트 키 삭제
        
        if value == "test_value":
            return True, "정상"
        else:
            return False, "캐시 동작 안됨"
    except Exception as e:
        return False, f"캐시 오류: {str(e)}"


def get_django_apps_status():
    """
    Django 앱들의 상태를 확인하는 함수
    
    Returns:
        dict: 각 앱의 상태 정보
    """
    apps_status = {}
    
    # Store 앱 확인
    try:
        from store.models import Product
        product_count = Product.objects.count()
        apps_status['store'] = {
            'status': '정상',
            'product_count': product_count,
            'model_accessible': True
        }
    except Exception as e:
        apps_status['store'] = {
            'status': f'오류: {str(e)}',
            'product_count': 0,
            'model_accessible': False
        }
    
    # Admin 앱 확인
    try:
        from django.contrib.admin.sites import site
        registered_models = len(site._registry)  # 등록된 모델 수
        apps_status['admin'] = {
            'status': '정상',
            'registered_models': registered_models,
            'admin_accessible': True
        }
    except Exception as e:
        apps_status['admin'] = {
            'status': f'오류: {str(e)}',
            'registered_models': 0,
            'admin_accessible': False
        }
    
    return apps_status


# =============================================================================
# API 엔드포인트들
# =============================================================================

@api_view(['GET'])
def system_health(request):
    """
    시스템 헬스체크 메인 엔드포인트
    
    통합 모니터링 대시보드에서 호출되는 메인 API입니다.
    시스템의 모든 상태 정보를 수집하여 JSON 형태로 반환합니다.
    
    Returns:
        Response: 시스템 상태 정보가 담긴 JSON 응답
    """
    global _last_history_time
    
    try:
        # =====================================================================
        # 1. 프로세스 정보 수집
        # =====================================================================
        current_process = psutil.Process()
        
        # CPU 사용률 (현재 프로세스 기준, 0.5초 간격으로 측정)
        cpu_percent = current_process.cpu_percent(interval=0.5)
        
        # 메모리 정보 (현재 프로세스 기준)
        memory_info = current_process.memory_info()
        memory_percent = current_process.memory_percent()
        
        # =====================================================================
        # 2. 시스템 전체 정보 (참고용)
        # =====================================================================
        system_mem = psutil.virtual_memory()
        system_cpu = psutil.cpu_percent(interval=0.5)
        
        # =====================================================================
        # 3. 기타 정보 수집
        # =====================================================================
        uptime = datetime.datetime.now() - datetime.datetime.fromtimestamp(psutil.boot_time())
        error_blocks = get_recent_error_blocks("logs/django.log")
        top_procs, total_mem = get_top_memory_processes(5)

        # =====================================================================
        # 4. 서비스 상태 확인
        # =====================================================================
        # 데이터베이스 연결 확인
        db_connected, db_status = check_database_connection()
        
        # 캐시 상태 확인
        cache_working, cache_status = check_cache_status()
        
        # Django 앱 상태 확인
        apps_status = get_django_apps_status()

        # =====================================================================
        # 5. 히스토리 업데이트 (1분마다)
        # =====================================================================
        now = datetime.datetime.now()
        data_point = {
            "cpu_percent": cpu_percent,
            "memory_percent": memory_percent,
            "timestamp": now.isoformat()
        }
        
        if not _last_history_time or (now - _last_history_time).total_seconds() >= 60:
            HEALTH_HISTORY.append(data_point)
            _last_history_time = now

        # =====================================================================
        # 6. 응답 데이터 구성
        # =====================================================================
        return Response({
            # 기본 메트릭
            "cpu_percent": cpu_percent,
            "system_cpu_percent": system_cpu,  # 시스템 전체 CPU (참고용)
            
            # 메모리 정보
            "memory": {
                "process_rss": memory_info.rss,  # 프로세스 메모리 사용량 (RSS)
                "process_percent": memory_percent,  # 프로세스 메모리 사용률
                "system_total": system_mem.total,  # 시스템 전체 메모리
                "system_used": system_mem.used,    # 시스템 사용 메모리
                "system_percent": system_mem.percent  # 시스템 메모리 사용률
            },
            
            # 시스템 정보
            "uptime": str(uptime),
            "recent_error_blocks": error_blocks,
            "timestamp": now.isoformat(),
            "history": list(HEALTH_HISTORY),
            
            # 프로세스 정보
            "top_memory_processes": top_procs,
            "total_memory": total_mem,
            
            # 서비스 정보
            "service_name": "Django Commerce",
            "service_port": 8000,
            
            # 컨테이너 정보
            "container_info": {
                "process_id": current_process.pid,
                "process_name": current_process.name(),
                "is_container": True
            },
            
            # 서비스 상태
            "database": {
                "connected": db_connected,
                "status": db_status
            },
            "cache": {
                "working": cache_working,
                "status": cache_status
            },
            "apps": apps_status,
            
            # Django 설정 정보
            "django_settings": {
                "debug": settings.DEBUG,
                "allowed_hosts": settings.ALLOWED_HOSTS,
                "static_root": settings.STATIC_ROOT,
                "media_root": getattr(settings, 'MEDIA_ROOT', 'Not configured')
            }
        })
    except Exception as e:
        # 오류 발생 시 500 에러와 함께 오류 정보 반환
        return Response({
            "error": f"시스템 정보 수집 중 오류 발생: {str(e)}",
            "timestamp": datetime.datetime.now().isoformat()
        }, status=500)


@api_view(['GET'])
def test_500(request):
    """
    테스트용 500 에러 엔드포인트
    
    통합 모니터링 대시보드에서 에러 처리 테스트를 위해 사용됩니다.
    
    Returns:
        Exception: 의도적으로 500 에러를 발생시킴
    """
    raise Exception("테스트용 500 에러 발생!") 