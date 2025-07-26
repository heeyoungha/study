# Django Admin 사용자 생성 가이드

## 1. 서비스 시작 후 Django Admin 접속

```bash
# 서비스 시작
./deploy.sh

# Django Admin 접속
https://localhost/commerce/admin/
```

## 2. 첫 번째 관리자 사용자 생성

### 방법 1: Django Shell 사용
```bash
# Django 컨테이너에 접속
docker exec -it django-commerce bash

# Django Shell 실행
python manage.py shell

# 관리자 사용자 생성
from django.contrib.auth.models import User
User.objects.create_superuser('admin', 'admin@example.com', 'your_password')
exit()
```

### 방법 2: Django Management Command 사용
```bash
# Django 컨테이너에 접속
docker exec -it django-commerce bash

# 관리자 사용자 생성
python manage.py createsuperuser
# Username: admin
# Email: admin@example.com
# Password: your_password
# Password (again): your_password
```

## 3. Django Admin에서 추가 사용자 생성

1. `https://localhost/commerce/admin/` 접속
2. 생성한 관리자 계정으로 로그인
3. **Users** 섹션에서 **ADD USER** 클릭
4. 사용자 정보 입력 후 저장

## 4. 권한 설정

### Django Admin에서 권한 부여:
1. **Users** → 사용자 선택
2. **Permissions** 섹션에서 필요한 권한 체크:
   - `Can add product` (상품 추가)
   - `Can change product` (상품 수정)
   - `Can delete product` (상품 삭제)
   - `Can view product` (상품 조회)

## 5. 운영 환경 권장사항

### 보안 강화:
- 강력한 비밀번호 사용
- 정기적인 비밀번호 변경
- 2FA (Two-Factor Authentication) 고려
- HTTPS 사용 필수

### 사용자 관리:
- 필요한 최소 권한만 부여
- 정기적인 사용자 계정 검토
- 퇴사자 계정 비활성화

## 6. 문제 해결

### MySQL 권한 오류:
```bash
# MySQL 데이터 디렉토리 권한 설정
sudo chown -R 999:999 data/mysql
```

### Django 마이그레이션 오류:
```bash
# Django 컨테이너에서 마이그레이션 실행
docker exec -it django-commerce python manage.py migrate
```

### 정적 파일 수집:
```bash
# Django 컨테이너에서 정적 파일 수집
docker exec -it django-commerce python manage.py collectstatic --noinput
``` 