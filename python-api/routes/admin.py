import re
from fastapi import APIRouter
from fastapi.responses import JSONResponse
import psutil
import datetime
import os
from collections import deque
from fastapi.responses import FileResponse

router = APIRouter()

HEALTH_HISTORY = deque(maxlen=30)
_last_history_time = None

def get_recent_error_blocks(log_path, minutes=30, max_lines=300):
    if not os.path.exists(log_path):
        return []
    now = datetime.datetime.now()
    result = []
    log_pattern = re.compile(r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}),\d+ (ERROR|CRITICAL) ")
    with open(log_path, 'r') as f:
        lines = f.readlines()[-max_lines:]
        block = []
        block_time = None
        for line in lines:
            m = log_pattern.match(line)
            if m:
                # 이전 블록 저장
                if block and block_time and (now - block_time).total_seconds() <= minutes * 60:
                    result.append(''.join(block).strip())
                # 새 블록 시작
                block = [line]
                try:
                    block_time = datetime.datetime.strptime(m.group(1), "%Y-%m-%d %H:%M:%S")
                except Exception:
                    block_time = None
            else:
                if block:
                    block.append(line)
        # 마지막 블록도 저장
        if block and block_time and (now - block_time).total_seconds() <= minutes * 60:
            result.append(''.join(block).strip())
    return result[-10:]  # 최근 10개만 반환

def get_recent_error_logs(log_path, minutes=30, max_lines=200):
    # 기존 줄 단위 파싱 함수(호환용, 사용 안 해도 됨)
    return []

def get_top_memory_processes(n=5):
    procs = []
    total_mem = psutil.virtual_memory().total
    for p in psutil.process_iter(['pid', 'name', 'memory_info']):
        try:
            mem = p.info['memory_info'].rss
            percent = (mem / total_mem) * 100 if total_mem else 0
            procs.append({
                'pid': p.info['pid'],
                'name': p.info['name'],
                'memory': mem,
                'memory_mb': round(mem / (1024 * 1024), 2),
                'percent_of_total': round(percent, 2)
            })
        except Exception:
            continue
    procs.sort(key=lambda x: x['memory'], reverse=True)
    return procs[:n], total_mem

@router.get("/python/admin/sys-health")
async def system_health():
    global _last_history_time
    cpu = psutil.cpu_percent(interval=0.5)
    mem = psutil.virtual_memory()
    uptime = datetime.datetime.now() - datetime.datetime.fromtimestamp(psutil.boot_time())
    error_blocks = get_recent_error_blocks("logs/app.log")
    top_procs, total_mem = get_top_memory_processes(5)

    now = datetime.datetime.now()
    data_point = {
        "cpu_percent": cpu,
        "memory_percent": mem.percent,
        "timestamp": now.isoformat()
    }
    if not _last_history_time or (now - _last_history_time).total_seconds() >= 60:
        HEALTH_HISTORY.append(data_point)
        _last_history_time = now

    return JSONResponse({
        "cpu_percent": cpu,
        "memory": {
            "total": mem.total,
            "used": mem.used,
            "percent": mem.percent
        },
        "uptime": str(uptime),
        "recent_error_blocks": error_blocks,
        "timestamp": now.isoformat(),
        "history": list(HEALTH_HISTORY),
        "top_memory_processes": top_procs,
        "total_memory": total_mem
    })

@router.get("/python/admin/test-500")
async def test_500():
    raise Exception("테스트용 500 에러 발생!")

@router.get("/python/check-health", response_class=FileResponse)
async def get_admin_sys_health():
    # admin-sys-health.html is located in python-api/static/
    static_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../static/admin-sys-health.html"))
    return FileResponse(static_path, media_type="text/html")