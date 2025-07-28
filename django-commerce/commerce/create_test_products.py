#!/usr/bin/env python3
"""
테스트용 상품 데이터 생성 스크립트
"""

import os
import sys
import django

# Django 설정 로드
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

from store.models import Product

def create_test_products():
    """테스트용 상품 데이터 생성"""
    
    # 기존 상품 삭제
    Product.objects.all().delete()
    
    # 테스트 상품 데이터
    products_data = [
        {
            'name': 'MacBook Pro 14인치',
            'description': 'Apple M3 Pro 칩을 탑재한 최신 MacBook Pro입니다. 전문적인 작업에 최적화되어 있습니다.',
            'price': 3500000,
            'stock': 10,
            'category': '전자제품',
            'is_active': True
        },
        {
            'name': 'Nike Air Max 270',
            'description': '편안한 착화감과 스타일리시한 디자인의 운동화입니다.',
            'price': 159000,
            'stock': 25,
            'category': '의류',
            'is_active': True
        },
        {
            'name': '파이썬 완전 가이드',
            'description': '파이썬 프로그래밍의 모든 것을 담은 완전 가이드입니다.',
            'price': 35000,
            'stock': 50,
            'category': '도서',
            'is_active': True
        },
        {
            'name': '스타벅스 원두 1kg',
            'description': '프리미엄 아라비카 원두로 만든 커피입니다.',
            'price': 25000,
            'stock': 30,
            'category': '식품',
            'is_active': True
        },
        {
            'name': '무선 블루투스 이어폰',
            'description': '노이즈 캔슬링 기능이 있는 프리미엄 무선 이어폰입니다.',
            'price': 180000,
            'stock': 15,
            'category': '전자제품',
            'is_active': True
        },
        {
            'name': '캐시미어 니트',
            'description': '부드럽고 따뜻한 캐시미어 소재의 니트 스웨터입니다.',
            'price': 89000,
            'stock': 20,
            'category': '의류',
            'is_active': True
        },
        {
            'name': '자바스크립트 핵심 가이드',
            'description': '모던 자바스크립트의 핵심 개념을 다루는 책입니다.',
            'price': 28000,
            'stock': 40,
            'category': '도서',
            'is_active': True
        },
        {
            'name': '유기농 바나나 1kg',
            'description': '유기농으로 재배된 신선한 바나나입니다.',
            'price': 8000,
            'stock': 100,
            'category': '식품',
            'is_active': True
        }
    ]
    
    # 상품 생성
    created_products = []
    for product_data in products_data:
        product = Product.objects.create(**product_data)
        created_products.append(product)
        print(f"상품 생성: {product.name} - ₩{product.price:,}")
    
    print(f"\n총 {len(created_products)}개의 테스트 상품이 생성되었습니다.")
    return created_products

if __name__ == '__main__':
    print("테스트용 상품 데이터를 생성합니다...")
    create_test_products()
    print("완료!") 