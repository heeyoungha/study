import React, { useState } from 'react';
import './App.css';
import ProductList from './components/ProductList';
import Cart from './components/Cart';

type Page = 'products' | 'cart';

function App() {
  const [currentPage, setCurrentPage] = useState<Page>('products');

  return (
    <div className="App">
      <nav className="commerce-nav">
        <div className="nav-container">
          <div className="nav-brand">
            <h2>🛍️ 커머스</h2>
          </div>
          <div className="nav-links">
            <button
              className={`nav-link ${currentPage === 'products' ? 'active' : ''}`}
              onClick={() => setCurrentPage('products')}
            >
              상품 목록
            </button>
            <button
              className={`nav-link ${currentPage === 'cart' ? 'active' : ''}`}
              onClick={() => setCurrentPage('cart')}
            >
              🛒 장바구니
            </button>
          </div>
        </div>
      </nav>

      <main className="commerce-main-content">
        {currentPage === 'products' && <ProductList />}
        {currentPage === 'cart' && <Cart />}
      </main>
    </div>
  );
}

export default App;
