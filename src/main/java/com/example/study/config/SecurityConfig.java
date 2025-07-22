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
import jakarta.servlet.http.Cookie;
import org.springframework.beans.factory.annotation.Autowired;

@Configuration
@EnableWebSecurity
@Slf4j
@RequiredArgsConstructor
public class SecurityConfig {

    private final CustomOAuth2UserService customOAuth2UserService;
    private final UserRepository userRepository;

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

            http
                    .oauth2Login((oauth2) -> oauth2
                            .loginPage("/login")
                            .userInfoEndpoint((userInfoEndpointConfig) ->
                                    userInfoEndpointConfig.userService(customOAuth2UserService))
                            .successHandler((request, response, authentication) -> {
                                try {
                                    log.info("OAuth2 Login successful");
                                    if (authentication == null) {
                                        log.error("authentication is null!");
                                        response.sendError(HttpServletResponse.SC_UNAUTHORIZED, "No authentication");
                                        return;
                                    }
                                    Object principal = authentication.getPrincipal();
                                    if (principal == null) {
                                        log.error("authentication.getPrincipal() is null!");
                                        response.sendError(HttpServletResponse.SC_UNAUTHORIZED, "No principal");
                                        return;
                                    }
                                    if (!(principal instanceof com.example.study.user.CustomOAuth2UserService.CustomOAuth2User)) {
                                        log.error("Principal is not instance of CustomOAuth2User!");
                                        response.sendError(HttpServletResponse.SC_UNAUTHORIZED, "Invalid principal type");
                                        return;
                                    }
                                    com.example.study.user.CustomOAuth2UserService.CustomOAuth2User oAuth2User =
                                            (com.example.study.user.CustomOAuth2UserService.CustomOAuth2User) principal;
                                    Long userId = oAuth2User.getUserId();

                                    if (userId == null) {
                                        log.error("userId is null!");
                                        response.sendError(HttpServletResponse.SC_UNAUTHORIZED, "No userId");
                                        return;
                                    }

                                    User user = userRepository.findById(userId).orElse(null);
                                    if (user == null) {
                                        log.error("User not found for userId: " + userId);
                                        response.sendError(HttpServletResponse.SC_UNAUTHORIZED, "User not found");
                                        return;
                                    }

                                    String jwt = customOAuth2UserService.generateJwtToken(user);
                                    
                                    // HTTPS 환경에서는 SameSite=None과 Secure 사용
                                    String cookieValue = String.format("jwt=%s; Path=/; Max-Age=%d; HttpOnly; SameSite=None; Secure", 
                                        jwt, 24*60*60);
                                    response.setHeader("Set-Cookie", cookieValue);

                                    HttpSession session = request.getSession();
                                    session.setAttribute("user", oAuth2User.getAttributes());
                                    // 로그인 후 리다이렉트
                                    response.sendRedirect("/");
                                } catch (IOException e) {
                                    log.error("Error during OAuth2 login success handling", e);
                                    response.sendError(HttpServletResponse.SC_INTERNAL_SERVER_ERROR,
                                            "Login redirect failed");
                                }
                            })
                    );

            // 정적 리소스 및 로그인 페이지에 대한 접근 허용 규칙
            http
                    .authorizeHttpRequests((auth) -> auth
                            .requestMatchers("/check-proto", "/", "/login", "/css/**", "/js/**", "/images/**", "/oauth2/**").permitAll()  // 모든 허용 경로를 한번에 설정
                            .anyRequest().authenticated());  // 그 외 모든 요청은 인증 필요

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

}
