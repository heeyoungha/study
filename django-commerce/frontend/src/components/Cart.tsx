import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../styles/commerce.css';

interface CartItem {
  id: number;
  product: {
    id: number;
    name: string;
    price: number;
    image?: string;
  };
  quantity: number;
  total_price: number;
}

interface CartData {
  id: number;
  items: CartItem[];
  total_price: number;
  item_count: number;
}

const Cart: React.FC = () => {
  const [cart, setCart] = useState<CartData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showModal, setShowModal] = useState(false);

  const API_BASE_URL = 'http://localhost:8002/store';

  // 장바구니 조회
  const fetchCart = async () => {
    try {
      setLoading(true);
      // TODO: 실제 인증 토큰을 사용해야 합니다
      const token = localStorage.getItem('authToken'); // 또는 다른 방식으로 토큰 가져오기
      const headers = token ? { Authorization: `Bearer ${token}` } : {};
      
      const response = await axios.get<CartData>(`${API_BASE_URL}/api/cart/`, { headers });
      console.log('Cart API response:', response.data);
      setCart(response.data);
      setError(null);
    } catch (err) {
      setError('장바구니를 불러오는 중 오류가 발생했습니다.');
      console.error('Error fetching cart:', err);
    } finally {
      setLoading(false);
    }
  };

  // 수량 변경
  const updateQuantity = async (itemId: number, quantity: number) => {
    try {
      // TODO: 실제 인증 토큰을 사용해야 합니다
      const token = localStorage.getItem('authToken'); // 또는 다른 방식으로 토큰 가져오기
      const headers = token ? { Authorization: `Bearer ${token}` } : {};
      
      await axios.patch<CartData>(`${API_BASE_URL}/api/cart/${itemId}/update/`, {
        quantity: quantity
      }, { headers });
      // 장바구니 다시 조회
      await fetchCart();
    } catch (err) {
      alert('수량 변경 중 오류가 발생했습니다.');
      console.error('Error updating quantity:', err);
    }
  };

  // 상품 제거
  const removeItem = async (itemId: number) => {
    try {
      // TODO: 실제 인증 토큰을 사용해야 합니다
      const token = localStorage.getItem('authToken'); // 또는 다른 방식으로 토큰 가져오기
      const headers = token ? { Authorization: `Bearer ${token}` } : {};
      
      const response = await axios.delete<CartData>(`${API_BASE_URL}/api/cart/${itemId}/remove/`, {
        data: { item_id: itemId },
        headers
      } as any);
      setCart(response.data);
    } catch (err) {
      console.error('Error removing item:', err);
    }
  };

  // 장바구니 비우기
  const clearCart = async () => {
    try {
      // TODO: 실제 인증 토큰을 사용해야 합니다
      const token = localStorage.getItem('authToken'); // 또는 다른 방식으로 토큰 가져오기
      const headers = token ? { Authorization: `Bearer ${token}` } : {};
      
      const response = await axios.delete<CartData>(`${API_BASE_URL}/api/cart/clear/`, { headers });
      setCart(response.data);
    } catch (err) {
      console.error('Error clearing cart:', err);
    }
  };

  // 주문하기
  const checkout = async () => {
    setShowModal(true);
  };

  useEffect(() => {
    fetchCart();
  }, []);

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('ko-KR').format(price);
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>장바구니를 불러오는 중...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="error-container">
        <p>{error}</p>
        <button onClick={fetchCart} className="retry-button">
          다시 시도
        </button>
      </div>
    );
  }

  if (!cart || !cart.items || cart.items.length === 0) {
    return (
      <div className="commerce-container">
        <div className="commerce-main">
          <div className="commerce-header">
            <h1>🛒 장바구니</h1>
            <p>장바구니가 비어있습니다</p>
          </div>
          <div className="empty-state">
            <h3>장바구니가 비어있습니다</h3>
            <p>상품을 추가해보세요!</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="commerce-container">
      <div className="commerce-main">
        <div className="commerce-header">
          <h1>🛒 장바구니</h1>
          <p>총 {cart.item_count || 0}개 상품</p>
        </div>

        <div className="cart-items">
          {cart.items && cart.items.map((item) => (
            <div key={item.id} className="cart-item">
              <div className="cart-item-image">
                {item.product.image ? (
                  <img src={item.product.image} alt={item.product.name} />
                ) : (
                  <div className="image-placeholder">이미지 없음</div>
                )}
              </div>
              
              <div className="cart-item-details">
                <h3 className="product-name">{item.product.name}</h3>
                <div className="price">₩{formatPrice(item.product.price)}</div>
                
                <div className="quantity-controls">
                  <button
                    className="quantity-btn"
                    onClick={() => updateQuantity(item.id, Math.max(1, item.quantity - 1))}
                    disabled={item.quantity <= 1}
                  >
                    -
                  </button>
                  <span className="quantity">{item.quantity}</span>
                  <button
                    className="quantity-btn"
                    onClick={() => updateQuantity(item.id, item.quantity + 1)}
                  >
                    +
                  </button>
                </div>
                
                <div className="item-total">
                  총: ₩{formatPrice(item.total_price)}
                </div>
              </div>
              
              <button
                className="remove-btn"
                onClick={() => removeItem(item.id)}
              >
                삭제
              </button>
            </div>
          ))}
        </div>

        <div className="cart-summary">
          <div className="summary-item">
            <span>상품 수:</span>
            <span>{cart.item_count || 0}개</span>
          </div>
          <div className="summary-item total">
            <span>총 금액:</span>
            <span className="price price-large">₩{formatPrice(cart.total_price || 0)}</span>
          </div>
        </div>

        <div className="cart-actions">
          <button className="btn btn-secondary" onClick={clearCart}>
            장바구니 비우기
          </button>
          <button className="btn btn-success" onClick={checkout}>
            주문하기
          </button>
        </div>
      </div>
      
      {/* 준비중 모달 */}
      {showModal && (
        <div className="modal-overlay" onClick={() => setShowModal(false)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <h3>🚧 준비중입니다</h3>
            <p>주문 기능은 현재 개발 중입니다.<br />조금만 기다려주세요!</p>
            <button className="btn btn-primary" onClick={() => setShowModal(false)}>
              확인
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Cart; 