// JWT 토큰을 쿠키에서 가져오는 함수
export const getAuthToken = (): string | null => {
  console.log('=== getAuthToken 디버깅 ===');
  console.log('1. 전체 쿠키:', document.cookie);
  
  // 쿠키에서 JWT 토큰 가져오기
  const cookies = document.cookie.split(';');
  console.log('2. 파싱된 쿠키 배열:', cookies);
  
  for (const cookie of cookies) {
    const [name, value] = cookie.trim().split('=');
    console.log('3. 쿠키 파싱:', { name, value });
    if (name === 'jwt') {
      console.log('4. JWT 쿠키 발견:', value ? '값 존재' : '값 없음');
      return value;
    }
  }
  
  console.log('5. JWT 쿠키 없음 - localStorage 확인');
  // localStorage에서도 확인 (fallback)
  const localToken = localStorage.getItem('authToken');
  console.log('6. localStorage 토큰:', localToken ? '존재' : '없음');
  return localToken;
};

// Authorization 헤더 생성
export const getAuthHeaders = (): Record<string, string> => {
  const token = getAuthToken();
  return token ? { Authorization: `Bearer ${token}` } : {};
};

// 로그인 상태 확인
export const isAuthenticated = (): boolean => {
  console.log('=== isAuthenticated 디버깅 ===');
  const token = getAuthToken();
  console.log('1. 토큰 존재 여부:', !!token);
  
  if (!token) {
    console.log('2. 토큰 없음 - 인증 실패');
    return false;
  }
  
  console.log('3. 토큰 발견 - 유효성 검증 시작');
  
  // JWT 토큰의 만료 시간 확인 (선택적)
  try {
    console.log('4. JWT 페이로드 파싱 시도');
    const payload = JSON.parse(atob(token.split('.')[1]));
    console.log('5. JWT 페이로드:', payload);
    
    const currentTime = Date.now() / 1000;
    console.log('6. 현재 시간:', currentTime);
    console.log('7. 토큰 만료 시간:', payload.exp);
    
    if (payload.exp && payload.exp < currentTime) {
      console.log('8. 토큰 만료됨');
      // 만료된 토큰 제거
      localStorage.removeItem('authToken');
      document.cookie = 'jwt=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
      return false;
    }
    
    console.log('9. 토큰 유효함, 만료 시간:', new Date(payload.exp * 1000));
    return true;
  } catch (error) {
    console.log('10. 토큰 검증 에러:', error);
    return false;
  }
};

// 로그인 페이지로 리다이렉트
export const redirectToLogin = (): void => {
  // Spring Boot 로그인 페이지로 리다이렉트
  window.location.href = '/login';
}; 