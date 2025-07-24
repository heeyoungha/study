package com.example.study;

import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class indexController {

    @GetMapping("/")
    public String index(Model model){
        Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
        String username = "Guest";
        
        if (authentication != null && authentication.isAuthenticated() && 
            !"anonymousUser".equals(authentication.getName())) {
            username = authentication.getName();
        }

        model.addAttribute("username", username);
        return "index";
    }

}
