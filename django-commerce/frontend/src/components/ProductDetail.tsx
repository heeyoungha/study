import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { getAuthHeaders, isAuthenticated, redirectToLogin } from '../utils/auth';
import '../styles/commerce.css';

interface Product {
  id: number;
  name: string;
  description: string;
  price: number;
  stock: number;
  category: string;
  image?: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

interface ProductDetailProps {
  productId: number;
  onBack: () => void;
}

const ProductDetail: React.FC<ProductDetailProps> = ({ productId, onBack }) => {
  const [product, setProduct] = useState<Product | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [quantity, setQuantity] = useState(1);

  const API_BASE_URL = '/commerce/store';

  useEffect(() => {
    const fetchProduct = async () => {
      try {
        setLoading(true);
        const response = await axios.get<Product>(`${API_BASE_URL}/api/products/${productId}/`);
        setProduct(response.data);
        setError(null);
      } catch (err) {
        setError('상품 정보를 불러오는 중 오류가 발생했습니다.');
        console.error('Error fetching product:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchProduct();
  }, [productId]);

  const handleQuantityChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = parseInt(e.target.value);
    if (value > 0 && value <= (product?.stock || 0)) {
      setQuantity(value);
    }
  };

  const addToCart = () => {
    if (!product) return;
    
    // 로그인 상태 확인
    if (!isAuthenticated()) {
      alert('로그인이 필요합니다. 로그인 후 다시 시도해주세요.');
      redirectToLogin();
      return;
    }
    
    // 로그인된 경우에만 API 호출
    const addToCartAsync = async () => {
      try {
        const headers = getAuthHeaders();
        
        await axios.post(`${API_BASE_URL}/api/cart/add/`, {
          product_id: product.id,
          quantity: quantity
        }, { headers });
        alert(`장바구니에 ${product.name} ${quantity}개가 추가되었습니다.`);
      } catch (err: any) {
        if (err.response?.status === 401) {
          alert('로그인이 필요합니다. 로그인 후 다시 시도해주세요.');
          redirectToLogin();
        } else {
          alert('장바구니 추가 중 오류가 발생했습니다.');
        }
        console.error('Error adding to cart:', err);
      }
    };

    addToCartAsync();
  };

  const handleDirectPurchase = () => {
    alert('바로 구매 기능은 준비 중입니다. 장바구니에 추가 후 구매해주세요.');
  };

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('ko-KR').format(price);
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('ko-KR');
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>상품 정보를 불러오는 중...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="error-container">
        <p>{error}</p>
        <button onClick={onBack} className="retry-button">
          목록으로 돌아가기
        </button>
      </div>
    );
  }

  if (!product) {
    return (
      <div className="error-container">
        <p>상품을 찾을 수 없습니다.</p>
        <button onClick={onBack} className="retry-button">
          목록으로 돌아가기
        </button>
      </div>
    );
  }

  return (
    <div className="commerce-container">
      <div className="commerce-main">
        <div className="commerce-header">
          <button onClick={onBack} className="back-button">
            ← 목록으로 돌아가기
          </button>
          <h1>상품 상세 정보</h1>
        </div>

        <div className="commerce-grid commerce-grid-2">
          <div className="product-image-section">
            <div className="product-image">
              {product.image ? (
                <img src={product.image} alt={product.name} />
              ) : (
                <div className="image-placeholder">이미지 없음</div>
              )}
            </div>
          </div>

          <div className="commerce-flex commerce-flex-column commerce-flex-gap-large">
            <div className="product-header">
              <h2 className="product-name">{product.name}</h2>
              <div className="product-category">{product.category}</div>
            </div>

            <div className="price price-large">
              ₩{formatPrice(product.price)}
            </div>

            <div className="commerce-section">
              <h3>상품 설명</h3>
              <p>{product.description}</p>
            </div>

            <div className="commerce-flex commerce-flex-gap">
              <span className="form-label">재고:</span>
              <span className={`status-badge ${product.stock > 0 ? 'status-success' : 'status-danger'}`}>
                {product.stock > 0 ? `${product.stock}개` : '품절'}
              </span>
            </div>

            <div className="meta-info">
              <div className="meta-item">
                <span className="meta-label">등록일:</span>
                <span className="meta-value">{formatDate(product.created_at)}</span>
              </div>
              <div className="meta-item">
                <span className="meta-label">수정일:</span>
                <span className="meta-value">{formatDate(product.updated_at)}</span>
              </div>
            </div>

            {product.stock > 0 && (
              <div className="commerce-section">
                <div className="form-group">
                  <label htmlFor="quantity" className="form-label">수량:</label>
                  <input
                    type="number"
                    id="quantity"
                    min="1"
                    max={product.stock}
                    value={quantity}
                    onChange={handleQuantityChange}
                    className="form-input"
                    style={{ width: '80px' }}
                  />
                </div>

                <div className="commerce-flex commerce-flex-between">
                  <span className="form-label">총 금액:</span>
                  <span className="price price-large">₩{formatPrice(product.price * quantity)}</span>
                </div>

                <div className="action-buttons">
                  <button 
                    className="btn btn-primary"
                    onClick={addToCart}
                    disabled={product.stock === 0}
                  >
                    장바구니에 추가
                  </button>
                  <button 
                    className="btn btn-success"
                    onClick={handleDirectPurchase}
                    disabled={product.stock === 0}
                  >
                    바로 구매
                  </button>
                </div>
              </div>
            )}

            {product.stock === 0 && (
              <div className="commerce-section">
                <p className="status-badge status-danger">현재 품절 상태입니다.</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProductDetail; 