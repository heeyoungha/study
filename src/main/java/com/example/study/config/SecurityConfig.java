package com.example.study.config;

import com.example.study.user.CustomOAuth2UserService;
import com.example.study.user.User;
import com.example.study.user.UserRepository;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpSession;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.oauth2.core.user.OAuth2User;
import org.springframework.security.web.SecurityFilterChain;
import lombok.RequiredArgsConstructor;
import java.io.IOException;
import java.util.Map;
import jakarta.servlet.http.Cookie;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;
import com.example.study.config.JwtAuthenticationFilter;
import org.springframework.security.web.authentication.AuthenticationSuccessHandler;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import org.springframework.security.core.Authentication;
import org.springframework.security.web.authentication.SimpleUrlAuthenticationSuccessHandler;
import java.io.IOException;

@Configuration
@EnableWebSecurity
@Slf4j
@RequiredArgsConstructor
public class SecurityConfig {

    private final CustomOAuth2UserService customOAuth2UserService;
    private final UserRepository userRepository;
    private final JwtAuthenticationFilter jwtAuthenticationFilter;

    @Value("${spring.profiles.active:local}")
    private String activeProfile;

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {

        try {

            log.info("Configuring Security Filter Chain");

            http
                    .csrf((csrf) -> csrf.disable());

            http
                    .formLogin((login) -> login.disable());

            http
                    .httpBasic((basic) -> basic.disable());

            // 세션 비활성화 (JWT 사용)
            http
                    .sessionManagement((session) -> session
                            .sessionCreationPolicy(SessionCreationPolicy.STATELESS));

            http
                    .oauth2Login((oauth2) -> oauth2
                            .loginPage("/login")
                            .userInfoEndpoint((userInfoEndpointConfig) ->
                                    userInfoEndpointConfig.userService(customOAuth2UserService))
                            .successHandler(oauth2AuthenticationSuccessHandler())
                    );

            // JWT 필터 추가
            http
                    .addFilterBefore(jwtAuthenticationFilter, UsernamePasswordAuthenticationFilter.class);

            // 정적 리소스 및 로그인 페이지에 대한 접근 허용 규칙
            http
                    .authorizeHttpRequests((auth) -> auth
                            .requestMatchers("/monitoring/**", "/unified-monitoring").permitAll()  // 모니터링 엔드포인트 명시적 허용
                            .requestMatchers("/check-proto", "/", "/login", "/css/**", "/js/**", "/images/**", "/oauth2/**", "/debug-all").permitAll()
                            .anyRequest().authenticated()
                            );  // 그 외 모든 요청은 인증 필요

            // HTTPS 인식을 위한 설정 (dev, prod 환경에서 적용)
            if ("dev".equals(activeProfile) || "prod".equals(activeProfile)) {
                log.info("Enabling HTTPS requirement for {} environment", activeProfile);
                http.requiresChannel(channel -> channel
                        .anyRequest().requiresSecure());
            }

            return http.build();

        } catch (Exception e) {
            log.error("Error configuring Security Filter Chain", e);
            throw e; // 중요한 설정 예외는 그대로 던져서 애플리케이션 시작을 막음
        }
    }

    @Bean
    public AuthenticationSuccessHandler oauth2AuthenticationSuccessHandler() {
        return new SimpleUrlAuthenticationSuccessHandler() {
            @Override
            public void onAuthenticationSuccess(HttpServletRequest request, 
                                            HttpServletResponse response, 
                                            Authentication authentication) throws IOException, ServletException {
                
                if (authentication.getPrincipal() instanceof CustomOAuth2UserService.CustomOAuth2User) {
                    CustomOAuth2UserService.CustomOAuth2User oauth2User = 
                        (CustomOAuth2UserService.CustomOAuth2User) authentication.getPrincipal();
                    
                    // JWT 토큰 생성
                    String jwt = customOAuth2UserService.generateJwtToken(oauth2User.getUserId());
                    
                    // JWT를 쿠키에 설정
                    Cookie jwtCookie = new Cookie("jwt", jwt);
                    jwtCookie.setHttpOnly(false);
                    jwtCookie.setSecure("dev".equals(activeProfile) || "prod".equals(activeProfile));
                    jwtCookie.setPath("/");
                    jwtCookie.setMaxAge(86400); // 24시간
                    response.addCookie(jwtCookie);
                }
                
                super.onAuthenticationSuccess(request, response, authentication);
            }
        };
    }
}
