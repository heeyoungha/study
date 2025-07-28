from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name='상품명')
    description = models.TextField(verbose_name='상품 설명')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='가격')
    stock = models.IntegerField(default=0, verbose_name='재고')
    image = models.ImageField(upload_to='products/', null=True, blank=True, verbose_name='상품 이미지')
    category = models.CharField(max_length=50, default='기타', verbose_name='카테고리')
    is_active = models.BooleanField(default=True, verbose_name='활성화')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='등록일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')
    
    class Meta:
        verbose_name = '상품'
        verbose_name_plural = '상품들'
    
    def __str__(self):
        return self.name

class Cart(models.Model):
    """장바구니 모델"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='사용자')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')
    
    class Meta:
        verbose_name = '장바구니'
        verbose_name_plural = '장바구니들'
    
    def __str__(self):
        return f"{self.user.username}의 장바구니"
    
    def get_total_price(self):
        """장바구니 총 금액 계산"""
        return sum(item.get_total_price() for item in self.cartitem_set.all())

class CartItem(models.Model):
    """장바구니 아이템 모델"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name='장바구니')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='상품')
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)], verbose_name='수량')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    
    class Meta:
        verbose_name = '장바구니 아이템'
        verbose_name_plural = '장바구니 아이템들'
        unique_together = ['cart', 'product']
    
    def __str__(self):
        return f"{self.cart.user.username} - {self.product.name} x{self.quantity}"
    
    def get_total_price(self):
        """아이템 총 금액 계산"""
        return self.product.price * self.quantity

class Order(models.Model):
    """주문 모델"""
    STATUS_CHOICES = [
        ('pending', '대기중'),
        ('confirmed', '확인됨'),
        ('shipped', '배송중'),
        ('delivered', '배송완료'),
        ('cancelled', '취소됨'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='사용자')
    order_number = models.CharField(max_length=20, unique=True, verbose_name='주문번호')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='주문상태')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='총 금액')
    shipping_address = models.TextField(verbose_name='배송주소')
    shipping_phone = models.CharField(max_length=20, verbose_name='연락처')
    payment_method = models.CharField(max_length=50, default='card', verbose_name='결제방법')
    payment_status = models.CharField(max_length=20, default='pending', verbose_name='결제상태')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='주문일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')
    
    class Meta:
        verbose_name = '주문'
        verbose_name_plural = '주문들'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.order_number} - {self.user.username}"
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            # 주문번호 자동 생성 (YYYYMMDD + 6자리 순번)
            from datetime import datetime
            today = datetime.now().strftime('%Y%m%d')
            last_order = Order.objects.filter(order_number__startswith=today).order_by('-order_number').first()
            if last_order:
                last_number = int(last_order.order_number[-6:])
                new_number = last_number + 1
            else:
                new_number = 1
            self.order_number = f"{today}{new_number:06d}"
        super().save(*args, **kwargs)

class OrderItem(models.Model):
    """주문 아이템 모델"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='주문')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='상품')
    quantity = models.PositiveIntegerField(verbose_name='수량')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='가격')
    
    class Meta:
        verbose_name = '주문 아이템'
        verbose_name_plural = '주문 아이템들'
    
    def __str__(self):
        return f"{self.order.order_number} - {self.product.name} x{self.quantity}"
    
    def get_total_price(self):
        """아이템 총 금액 계산"""
        return self.price * self.quantity
