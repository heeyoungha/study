package com.example.study.config;

import com.example.study.user.User;
import com.example.study.user.UserRepository;
import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.security.Keys;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.Cookie;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import javax.crypto.SecretKey;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.Collections;
import java.util.Optional;

@Component
@RequiredArgsConstructor
@Slf4j
public class JwtAuthenticationFilter extends OncePerRequestFilter {

    private final UserRepository userRepository;

    @Override
    protected void doFilterInternal(HttpServletRequest request, 
                                  HttpServletResponse response, 
                                  FilterChain filterChain) throws ServletException, IOException {
        
        try {
            // JWT 토큰 추출
            String jwt = extractJwtFromRequest(request);
            
            if (jwt != null && validateJwtToken(jwt)) {
                // JWT에서 사용자 정보 추출
                Claims claims = getClaimsFromToken(jwt);
                Long userId = Long.parseLong(claims.getSubject());
                
                // 사용자 정보 조회
                Optional<User> userOpt = userRepository.findById(userId);
                if (userOpt.isPresent()) {
                    User user = userOpt.get();
                    
                    // 인증 객체 생성
                    UsernamePasswordAuthenticationToken authentication = 
                        new UsernamePasswordAuthenticationToken(
                            user.getUsername(),
                            null,
                            Collections.singletonList(new SimpleGrantedAuthority(user.getRole()))
                        );
                    
                    // SecurityContext에 인증 정보 설정
                    SecurityContextHolder.getContext().setAuthentication(authentication);
                    log.debug("JWT 인증 성공: {}", user.getUsername());
                }
            }
        } catch (Exception e) {
            log.warn("JWT 인증 실패: {}", e.getMessage());
        }
        
        filterChain.doFilter(request, response);
    }

    private String extractJwtFromRequest(HttpServletRequest request) {
        // 쿠키에서 JWT 추출
        Cookie[] cookies = request.getCookies();
        if (cookies != null) {
            for (Cookie cookie : cookies) {
                if ("jwt".equals(cookie.getName())) {
                    return cookie.getValue();
                }
            }
        }
        
        // Authorization 헤더에서 JWT 추출 (Bearer 토큰)
        String authHeader = request.getHeader("Authorization");
        if (authHeader != null && authHeader.startsWith("Bearer ")) {
            return authHeader.substring(7);
        }
        
        return null;
    }

    private boolean validateJwtToken(String token) {
        try {
            String secret = System.getenv("JWT_SECRET_KEY");
            if (secret == null) {
                log.error("JWT_SECRET_KEY 환경변수가 설정되지 않았습니다.");
                return false;
            }
            
            SecretKey key = Keys.hmacShaKeyFor(secret.getBytes(StandardCharsets.UTF_8));
            Jwts.parserBuilder()
                .setSigningKey(key)
                .build()
                .parseClaimsJws(token);
            
            return true;
        } catch (Exception e) {
            log.warn("JWT 토큰 검증 실패: {}", e.getMessage());
            return false;
        }
    }

    private Claims getClaimsFromToken(String token) {
        String secret = System.getenv("JWT_SECRET_KEY");
        SecretKey key = Keys.hmacShaKeyFor(secret.getBytes(StandardCharsets.UTF_8));
        
        return Jwts.parserBuilder()
            .setSigningKey(key)
            .build()
            .parseClaimsJws(token)
            .getBody();
    }
} 