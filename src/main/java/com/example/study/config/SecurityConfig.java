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
                            .defaultSuccessUrl("/", true)
                    );

            // 정적 리소스 및 로그인 페이지에 대한 접근 허용 규칙
            http
                    .authorizeHttpRequests((auth) -> auth
                            .requestMatchers("/check-proto", "/", "/login", "/css/**", "/js/**", "/images/**", "/oauth2/**", "/debug-all","/project/**").permitAll()  // 모든 허용 경로를 한번에 설정
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

}
