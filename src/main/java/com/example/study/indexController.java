package com.example.study;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@Controller
public class indexController {

    @GetMapping("/v1")
    public String helloworld(){
        return "index";
    }

}
