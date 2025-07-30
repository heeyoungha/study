from django.urls import path
from . import views

urlpatterns = [
    # 템플릿 페이지
    path('products/', views.product_list_page, name='product_list_page'),
    
    # 상품 관련 API
    path('api/products/', views.product_list, name='product_list'),
    path('api/products/<int:id>/', views.product_detail, name='product_detail'),
    path('api/products/categories/', views.product_categories, name='product_categories'),
    path('api/products/search/', views.product_search, name='product_search'),
    
    # 장바구니 관련 API
    path('api/cart/', views.cart_view, name='cart_view'),
    path('api/cart/add/', views.cart_add_item, name='cart_add_item'),
    path('api/cart/<int:item_id>/update/', views.cart_update_item, name='cart_update_item'),
    path('api/cart/<int:item_id>/remove/', views.cart_remove_item, name='cart_remove_item'),
    path('api/cart/clear/', views.cart_clear, name='cart_clear'),
    
    # 주문 관련 API
    path('api/checkout/', views.checkout_view, name='checkout_view'),
    path('api/orders/', views.order_list_view, name='order_list_view'),
    path('api/orders/<int:order_id>/', views.order_detail_view, name='order_detail_view'),
] 