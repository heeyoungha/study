package com.example.study;

import jakarta.servlet.http.HttpSession;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@Controller
public class indexController {

    @GetMapping("/v1")
    public String helloworld(HttpSession session, Model model){
        String username = (String) session.getAttribute("username");

        if(username == null) {
            username = "Guest";
        }

        model.addAttribute("username", username);

        return "index";
    }

}
