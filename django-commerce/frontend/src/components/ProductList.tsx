import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import ProductDetail from './ProductDetail';
import { getAuthHeaders, getAuthToken, isAuthenticated, redirectToLogin } from '../utils/auth';
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
  console.log('🚀 ProductList 컴포넌트 렌더링');
  
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');
  const [selectedProductId, setSelectedProductId] = useState<number | null>(null);

  const API_BASE_URL = '/commerce/store';

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
  const addToCart = (productId: number) => {
    console.log('🔥 addToCart 함수 호출됨!');
    console.log('=== 장바구니 추가 디버깅 시작 ===');
    console.log('Product ID:', productId);
    console.log('API Base URL:', API_BASE_URL);
    
    // 로그인 상태 확인
    console.log('1. 인증 상태 확인 중...');
    const isAuth = isAuthenticated();
    console.log('2. 인증 결과:', isAuth);
    
    // 토큰 정보 확인
    const token = getAuthToken();
    console.log('3. 토큰 정보:', token ? '토큰 존재' : '토큰 없음');
    if (token) {
      console.log('4. 토큰 길이:', token.length);
      console.log('5. 토큰 시작 부분:', token.substring(0, 20) + '...');
    }
    
    if (!isAuth) {
      console.log('6. 인증 실패 - 로그인 페이지로 이동');
      alert('로그인이 필요합니다. 로그인 후 다시 시도해주세요.');
      redirectToLogin();
      return;
    }

    console.log('7. 인증 성공 - API 호출 준비');
    
    // 로그인된 경우에만 API 호출
    const addToCartAsync = async () => {
      try {
        console.log('8. 인증 헤더 생성 중...');
        const headers = getAuthHeaders();
        console.log('9. 생성된 헤더:', headers);
        
        // 토큰이 없으면 API 호출하지 않음
        if (!headers.Authorization) {
          console.log('10. Authorization 헤더 없음 - 로그인 페이지로 이동');
          alert('로그인이 필요합니다. 로그인 후 다시 시도해주세요.');
          redirectToLogin();
          return;
        }
        
        console.log('11. API 요청 데이터 준비');
        const requestData = {
          product_id: productId,
          quantity: 1
        };
        console.log('12. 요청 데이터:', requestData);
        console.log('13. 요청 URL:', `${API_BASE_URL}/api/cart/add/`);
        console.log('14. 요청 헤더:', headers);
        
        console.log('15. API 호출 시작...');
        const response = await axios.post(`${API_BASE_URL}/api/cart/add/`, requestData, { headers });
        console.log('16. API 호출 성공:', response.data);
        alert('장바구니에 추가되었습니다!');
      } catch (err: any) {
        console.log('17. API 호출 실패');
        console.log('18. 에러 타입:', err.constructor.name);
        console.log('19. 에러 메시지:', err.message);
        console.log('20. 에러 응답 상태:', err.response?.status);
        console.log('21. 에러 응답 데이터:', err.response?.data);
        console.log('22. 에러 응답 헤더:', err.response?.headers);
        console.log('23. 전체 에러 객체:', err);
        
        if (err.response?.status === 401) {
          console.log('24. 401 Unauthorized 에러 - 로그인 페이지로 이동');
          alert('로그인이 필요합니다. 로그인 후 다시 시도해주세요.');
          redirectToLogin();
        } else {
          console.log('25. 기타 에러');
          alert('장바구니 추가 중 오류가 발생했습니다.');
        }
        console.error('Error adding to cart:', err);
      }
    };

    console.log('26. 비동기 함수 호출');
    addToCartAsync();
    console.log('27. === 장바구니 추가 디버깅 완료 ===');
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
                      onClick={() => {
                        console.log('=== 장바구니 버튼 클릭 ===');
                        console.log('클릭된 상품 ID:', product.id);
                        console.log('상품명:', product.name);
                        addToCart(product.id);
                      }}
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