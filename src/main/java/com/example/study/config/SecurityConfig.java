package com.example.study.config;

import com.example.study.user.CustomOAuth2UserService;
import jakarta.servlet.http.HttpSession;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.oauth2.core.user.OAuth2User;
import org.springframework.security.web.SecurityFilterChain;

@Configuration
@EnableWebSecurity
public class SecurityConfig {

    private final CustomOAuth2UserService customOAuth2UserService;

    public SecurityConfig(CustomOAuth2UserService customOAuth2UserService) {
        this.customOAuth2UserService = customOAuth2UserService;
    }


    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {

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
                            // 성공적인 OAuth2 로그인 후 세션에 사용자 정보를 저장
                            OAuth2User oAuth2User = (OAuth2User) authentication.getPrincipal();
                            HttpSession session = request.getSession();
                            session.setAttribute("user", oAuth2User.getAttributes());

                            // 로그인 후 리다이렉트
                            response.sendRedirect("/v1");
                        })
                );

        // 정적 리소스 및 로그인 페이지에 대한 접근 허용 규칙
        http
                .authorizeHttpRequests((auth) -> auth
                        .requestMatchers("/", "/login", "/css/**", "/js/**", "/images/**").permitAll()  // 정적 리소스 경로 허용
                        .requestMatchers("/oauth2/**").permitAll()  // OAuth2 관련 경로 허용
                        .anyRequest().authenticated());  // 그 외 모든 요청은 인증 필요

        return http.build();
    }

}
