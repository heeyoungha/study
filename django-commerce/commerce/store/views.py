from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from .models import Product, Cart, CartItem, Order, OrderItem
from .serializers import (
    ProductSerializer, CartSerializer, CartItemSerializer, 
    OrderSerializer, OrderItemSerializer, UserSerializer
)
import json

# 상품 관련 API
@extend_schema(
    tags=['products'],
    summary='상품 목록 조회',
    description='활성화된 모든 상품의 목록을 조회합니다.',
    responses={200: ProductSerializer(many=True)}
)
@api_view(['GET'])
def product_list(request):
    """상품 목록 조회"""
    products = Product.objects.filter(is_active=True)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@extend_schema(
    tags=['products'],
    summary='상품 상세 조회',
    description='특정 상품의 상세 정보를 조회합니다.',
    parameters=[OpenApiParameter(name='id', location=OpenApiParameter.PATH, required=True, type=int)],
    responses={200: ProductSerializer}
)
@api_view(['GET'])
def product_detail(request, id):
    """상품 상세 조회"""
    product = get_object_or_404(Product, id=id, is_active=True)
    serializer = ProductSerializer(product)
    return Response(serializer.data)

@extend_schema(
    tags=['products'],
    summary='카테고리별 상품 조회',
    description='특정 카테고리의 상품들을 조회합니다.',
    parameters=[OpenApiParameter(name='category', location=OpenApiParameter.QUERY, required=True, type=str)],
    responses={200: ProductSerializer(many=True)}
)
@api_view(['GET'])
def product_categories(request):
    """카테고리별 상품 조회"""
    category = request.GET.get('category')
    if category:
        products = Product.objects.filter(category=category, is_active=True)
    else:
        products = Product.objects.filter(is_active=True)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@extend_schema(
    tags=['products'],
    summary='상품 검색',
    description='상품명으로 상품을 검색합니다.',
    parameters=[OpenApiParameter(name='q', location=OpenApiParameter.QUERY, required=True, type=str)],
    responses={200: ProductSerializer(many=True)}
)
@api_view(['GET'])
def product_search(request):
    """상품 검색"""
    query = request.GET.get('q', '')
    if query:
        products = Product.objects.filter(name__icontains=query, is_active=True)
    else:
        products = Product.objects.filter(is_active=True)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

# 장바구니 관련 API
@extend_schema(
    tags=['cart'],
    summary='장바구니 조회',
    description='현재 사용자의 장바구니를 조회합니다.',
    responses={200: CartSerializer}
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cart_view(request):
    """장바구니 조회"""
    cart, created = Cart.objects.get_or_create(user=request.user)
    serializer = CartSerializer(cart)
    return Response(serializer.data)

@extend_schema(
    tags=['cart'],
    summary='장바구니에 상품 추가',
    description='장바구니에 상품을 추가합니다.',
    request=CartItemSerializer,
    responses={201: CartItemSerializer}
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cart_add_item(request):
    """장바구니에 상품 추가"""
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    product_id = request.data.get('product_id')
    quantity = request.data.get('quantity', 1)
    
    if not product_id:
        return Response({'error': 'product_id is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        product = Product.objects.get(id=product_id, is_active=True)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # 기존 아이템이 있는지 확인
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart, 
        product=product,
        defaults={'quantity': quantity}
    )
    
    if not created:
        cart_item.quantity += quantity
        cart_item.save()
    
    serializer = CartItemSerializer(cart_item)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@extend_schema(
    tags=['cart'],
    summary='장바구니 아이템 수량 변경',
    description='장바구니 아이템의 수량을 변경합니다.',
    parameters=[OpenApiParameter(name='item_id', location=OpenApiParameter.PATH, required=True, type=int)],
    request=CartItemSerializer,
    responses={200: CartItemSerializer}
)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def cart_update_item(request, item_id):
    """장바구니 아이템 수량 변경"""
    try:
        cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
    except CartItem.DoesNotExist:
        return Response({'error': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)
    
    quantity = request.data.get('quantity')
    if quantity is None or quantity < 1:
        return Response({'error': 'Valid quantity is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    cart_item.quantity = quantity
    cart_item.save()
    
    serializer = CartItemSerializer(cart_item)
    return Response(serializer.data)

@extend_schema(
    tags=['cart'],
    summary='장바구니 아이템 삭제',
    description='장바구니에서 아이템을 삭제합니다.',
    parameters=[OpenApiParameter(name='item_id', location=OpenApiParameter.PATH, required=True, type=int)],
    responses={204: None}
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def cart_remove_item(request, item_id):
    """장바구니 아이템 삭제"""
    try:
        cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
    except CartItem.DoesNotExist:
        return Response({'error': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)
    
    cart_item.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# 주문 관련 API
@extend_schema(
    tags=['orders'],
    summary='주문 생성',
    description='장바구니의 상품들로 주문을 생성합니다.',
    request=OrderSerializer,
    responses={201: OrderSerializer}
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def checkout_view(request):
    """주문 생성"""
    cart = Cart.objects.filter(user=request.user).first()
    if not cart or cart.cartitem_set.count() == 0:
        return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)
    
    # 주문 데이터
    shipping_address = request.data.get('shipping_address')
    shipping_phone = request.data.get('shipping_phone')
    payment_method = request.data.get('payment_method', 'card')
    
    if not shipping_address or not shipping_phone:
        return Response({'error': 'shipping_address and shipping_phone are required'}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    # 주문 생성
    order = Order.objects.create(
        user=request.user,
        total_amount=cart.get_total_price(),
        shipping_address=shipping_address,
        shipping_phone=shipping_phone,
        payment_method=payment_method
    )
    
    # 주문 아이템 생성
    for cart_item in cart.cartitem_set.all():
        OrderItem.objects.create(
            order=order,
            product=cart_item.product,
            quantity=cart_item.quantity,
            price=cart_item.product.price
        )
    
    # 장바구니 비우기
    cart.cartitem_set.all().delete()
    
    serializer = OrderSerializer(order)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@extend_schema(
    tags=['orders'],
    summary='주문 목록 조회',
    description='현재 사용자의 주문 목록을 조회합니다.',
    responses={200: OrderSerializer(many=True)}
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_list_view(request):
    """주문 목록 조회"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

@extend_schema(
    tags=['orders'],
    summary='주문 상세 조회',
    description='특정 주문의 상세 정보를 조회합니다.',
    parameters=[OpenApiParameter(name='order_id', location=OpenApiParameter.PATH, required=True, type=int)],
    responses={200: OrderSerializer}
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_detail_view(request, order_id):
    """주문 상세 조회"""
    try:
        order = Order.objects.get(id=order_id, user=request.user)
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = OrderSerializer(order)
    return Response(serializer.data)

# 템플릿 렌더링 뷰
def product_list_page(request):
    """상품 목록 페이지 렌더링"""
    return render(request, 'store/product_list.html')
