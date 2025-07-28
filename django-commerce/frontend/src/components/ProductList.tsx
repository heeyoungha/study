import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import ProductDetail from './ProductDetail';
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
}

const ProductList: React.FC = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');
  const [selectedProductId, setSelectedProductId] = useState<number | null>(null);

  const API_BASE_URL = 'http://localhost:8002/store';

  // 상품 목록 가져오기
  const fetchProducts = useCallback(async () => {
    try {
      setLoading(true);
      const response = await axios.get<Product[]>(`${API_BASE_URL}/api/products/`);
      setProducts(response.data);
      setError(null);
    } catch (err) {
      setError('상품 목록을 불러오는 중 오류가 발생했습니다.');
      console.error('Error fetching products:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  // 상품 검색
  const searchProducts = useCallback(async () => {
    if (!searchTerm.trim()) {
      fetchProducts();
      return;
    }

    try {
      setLoading(true);
      const response = await axios.get<Product[]>(`${API_BASE_URL}/api/products/search/?q=${encodeURIComponent(searchTerm)}`);
      setProducts(response.data);
      setError(null);
    } catch (err) {
      setError('검색 중 오류가 발생했습니다.');
      console.error('Error searching products:', err);
    } finally {
      setLoading(false);
    }
  }, [searchTerm, fetchProducts]);

  // 카테고리 필터
  const filterByCategory = useCallback(async () => {
    if (!selectedCategory) {
      fetchProducts();
      return;
    }

    try {
      setLoading(true);
      const response = await axios.get<Product[]>(`${API_BASE_URL}/api/products/categories/?category=${encodeURIComponent(selectedCategory)}`);
      setProducts(response.data);
      setError(null);
    } catch (err) {
      setError('필터링 중 오류가 발생했습니다.');
      console.error('Error filtering products:', err);
    } finally {
      setLoading(false);
    }
  }, [selectedCategory, fetchProducts]);

  // 상품 상세보기
  const viewProduct = (productId: number) => {
    setSelectedProductId(productId);
  };

  // 장바구니에 추가
  const addToCart = async (productId: number) => {
    try {
      // TODO: 실제 인증 토큰을 사용해야 합니다
      const token = localStorage.getItem('authToken'); // 또는 다른 방식으로 토큰 가져오기
      const headers = token ? { Authorization: `Bearer ${token}` } : {};
      
      await axios.post(`${API_BASE_URL}/api/cart/add/`, {
        product_id: productId,
        quantity: 1
      }, { headers });
      alert('장바구니에 추가되었습니다!');
    } catch (err) {
      alert('장바구니 추가 중 오류가 발생했습니다.');
      console.error('Error adding to cart:', err);
    }
  };

  // 컴포넌트 마운트 시 상품 목록 가져오기
  useEffect(() => {
    fetchProducts();
  }, [fetchProducts]);

  // 검색어 변경 시 검색
  useEffect(() => {
    const timeoutId = setTimeout(() => {
      if (searchTerm) {
        searchProducts();
      } else {
        fetchProducts();
      }
    }, 500);

    return () => clearTimeout(timeoutId);
  }, [searchTerm, searchProducts, fetchProducts]);

  // 카테고리 변경 시 필터
  useEffect(() => {
    if (selectedCategory !== undefined) {
      filterByCategory();
    }
  }, [selectedCategory, filterByCategory]);

  // 상품 상세 페이지 표시
  if (selectedProductId) {
    return (
      <ProductDetail 
        productId={selectedProductId} 
        onBack={() => setSelectedProductId(null)} 
      />
    );
  }

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>상품을 불러오는 중...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="error-container">
        <p>{error}</p>
        <button onClick={fetchProducts} className="retry-button">
          다시 시도
        </button>
      </div>
    );
  }

  return (
    <div className="commerce-container">
      <div className="commerce-main">
        <div className="commerce-header">
          <h1>🛒 상품 목록</h1>
          <p>다양한 상품들을 둘러보세요</p>
        </div>

        <div className="controls">
          <div className="search-box">
            <input
              type="text"
              placeholder="상품명을 입력하세요..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          <div className="category-filter">
            <label htmlFor="categorySelect">카테고리:</label>
            <select
              id="categorySelect"
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
            >
              <option value="">전체</option>
              <option value="전자제품">전자제품</option>
              <option value="의류">의류</option>
              <option value="도서">도서</option>
              <option value="식품">식품</option>
              <option value="기타">기타</option>
            </select>
          </div>
        </div>

        {products.length === 0 ? (
          <div className="empty-state">
            <h3>상품이 없습니다</h3>
            <p>등록된 상품이 없습니다.</p>
          </div>
        ) : (
          <div className="commerce-grid commerce-grid-auto">
            {products.map((product) => (
              <div key={product.id} className="commerce-card">
                <div className="product-image">
                  {product.image ? (
                    <img src={product.image} alt={product.name} />
                  ) : (
                    <div className="image-placeholder">이미지 없음</div>
                  )}
                </div>
                <div className="commerce-card-body">
                  <h3 className="product-name">{product.name}</h3>
                  <p className="product-description">{product.description}</p>
                  <div className="price price-medium">₩{product.price.toLocaleString()}</div>
                  <div className="product-stock">재고: {product.stock}개</div>
                  <div className="action-buttons">
                    <button
                      className="btn btn-primary"
                      onClick={() => viewProduct(product.id)}
                    >
                      상세보기
                    </button>
                    <button
                      className="btn btn-success"
                      onClick={() => addToCart(product.id)}
                    >
                      장바구니
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default ProductList; 