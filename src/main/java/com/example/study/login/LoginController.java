package com.example.study.login;

import jakarta.servlet.http.HttpServletRequest;
import org.springframework.core.io.ClassPathResource;
import org.springframework.core.io.Resource;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.http.MediaType;

@Controller
public class LoginController {

    @GetMapping("/")
    public String home() {
        return "redirect:/login";
    }
    @GetMapping("/login")
    public String login(){
        return "login/login";
    }
    @GetMapping("/css/**")
    public ResponseEntity<Resource> serveCss(HttpServletRequest request) {
        String cssFile = request.getRequestURI().substring(request.getContextPath().length());
        Resource resource = new ClassPathResource("static" + cssFile); // 리소스 경로 지정
        return ResponseEntity.ok()
                .contentType(MediaType.valueOf("text/css")) // MIME 타입 설정
                .body(resource);
    }
}
