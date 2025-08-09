#!/usr/bin/env python3
"""
테스트용 실천 지원 상품 데이터 생성 스크립트
"""

import os
import sys
import django

# Django 설정 로드
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

from store.models import Product

def create_test_products():
    """테스트용 실천 지원 상품 데이터 생성"""
    
    # 기존 상품 삭제
    Product.objects.all().delete()
    
    products_data = [
        {
            'name': '매일 회고 일기장 세트',
            'description': '하루를 돌아보고 실행 계획을 적을 수 있도록 구성된 3개월 분량의 프리미엄 회고 일기장과 펜 세트입니다.',
            'price': 25000,
            'stock': 50,
            'category': '문구',
            'is_active': True
        },
        {
            'name': '독서 모임 정기 구독권 (1개월)',
            'description': '매주 1회 진행되는 온라인 독서 토론 모임 참여권. 회고 기반 질문과 실천 과제를 제공합니다.',
            'price': 39000,
            'stock': 100,
            'category': '서비스',
            'is_active': True
        },
        {
            'name': '명상·마음챙김 오디오 가이드',
            'description': '아침 10분 명상을 돕는 전문 강사의 오디오 가이드와 배경음 패키지.',
            'price': 15000,
            'stock': 200,
            'category': '디지털콘텐츠',
            'is_active': True
        },
        {
            'name': '실천 습관 관리 앱 프리미엄 6개월 이용권',
            'description': '회고에서 나온 실천 목표를 체계적으로 관리할 수 있는 앱의 프리미엄 버전 이용권입니다.',
            'price': 49000,
            'stock': 300,
            'category': '디지털서비스',
            'is_active': True
        },
        {
            'name': '감사 일기 전용 노트',
            'description': '매일 감사한 일을 적을 수 있도록 설계된 하루 3문항 구성의 노트. 긍정적인 마음가짐을 형성합니다.',
            'price': 12000,
            'stock': 80,
            'category': '문구',
            'is_active': True
        },
        {
            'name': '사이드 프로젝트 기획 워크숍',
            'description': '회고에서 도출한 아이디어를 바탕으로 한 달 내 실행 가능한 프로젝트를 설계하는 4주 과정.',
            'price': 89000,
            'stock': 30,
            'category': '교육',
            'is_active': True
        },
        {
            'name': '자기계발 도서 패키지',
            'description': '목표 달성을 위한 필독서 3권 세트. 실천 과제와 함께 제공됩니다.',
            'price': 45000,
            'stock': 40,
            'category': '도서',
            'is_active': True
        },
        {
            'name': '집중력 향상 카페인 프리 티 세트',
            'description': '밤에도 편안하게 마실 수 있는 허브 블렌드 티 5종 세트. 독서와 회고 시간에 적합합니다.',
            'price': 22000,
            'stock': 60,
            'category': '식품',
            'is_active': True
        }
    ]
    
    created_products = []
    for product_data in products_data:
        product = Product.objects.create(**product_data)
        created_products.append(product)
        print(f"상품 생성: {product.name} - ₩{product.price:,}")
    
    print(f"\n총 {len(created_products)}개의 테스트 상품이 생성되었습니다.")
    return created_products

if __name__ == '__main__':
    print("테스트용 실천 지원 상품 데이터를 생성합니다...")
    create_test_products()
    print("완료!") 
