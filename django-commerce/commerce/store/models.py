from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name='상품명')
    description = models.TextField(verbose_name='상품 설명')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='가격')
    stock = models.IntegerField(default=0, verbose_name='재고')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='등록일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')
    
    class Meta:
        verbose_name = '상품'
        verbose_name_plural = '상품들'
    
    def __str__(self):
        return self.name
