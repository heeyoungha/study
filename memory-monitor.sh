#!/bin/bash

echo "=== 메모리 사용량 모니터링 ==="
echo ""

# 전체 메모리 정보
echo "📊 전체 메모리 정보:"
vm_stat | grep -E "(Pages free|Pages active|Pages inactive|Pages wired down|Pages purgeable)"
echo ""

# 메모리 사용량 상위 프로세스
echo "🔝 메모리 사용량 상위 프로세스:"
ps -eo pid,comm,%mem | sort -k3 -nr | head -10
echo ""

# 메모리 정리 옵션
echo "🧹 메모리 정리 옵션:"
echo "1. 캐시 정리: sudo purge"
echo "2. 불필요한 프로세스 종료: killall [프로세스명]"
echo "3. Docker 컨테이너 정리: docker system prune"
echo "4. Docker 볼륨 정리: docker volume prune"
echo ""

# 현재 메모리 사용률
echo "📈 현재 메모리 사용률:"
top -l 1 | grep "PhysMem"
echo ""

# 권장사항
echo "💡 메모리 관리 권장사항:"
echo "- 큰 메모리를 사용하는 프로세스 확인"
echo "- 불필요한 애플리케이션 종료"
echo "- Docker 컨테이너 정리"
echo "- 브라우저 탭 정리"
echo "- IDE에서 불필요한 프로젝트 닫기" 