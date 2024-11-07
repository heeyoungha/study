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
            .csrf((csrf) -> csrf.disable())
            .formLogin((login) -> login.disable())
            .httpBasic((basic) -> basic.disable());

        http
            .oauth2Login(oauth2 -> oauth2
                    .loginPage("/login")
                    .defaultSuccessUrl("/", true)
                    .userInfoEndpoint(userInfo -> userInfo
                            .userService(customOAuth2UserService))
                    .authorizationEndpoint(authorization -> authorization
                            .baseUri("/oauth2/authorization"))
                    .redirectionEndpoint(redirection -> redirection
                            .baseUri("https://letsadam.link/login/oauth2/code/*"))
            );


        // 정적 리소스 및 로그인 페이지에 대한 접근 허용 규칙
        http
                .authorizeHttpRequests((auth) -> auth
                .requestMatchers("/", "/css/**", "/js/**", "/images/**")
                .permitAll()
                .requestMatchers("/login")
                .anonymous()
                .anyRequest().authenticated());
        return http.build();
    }

}
