package com.example.study.mindmap;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class MindMap {

    @GetMapping("/mindmap")
    public String index(){
        //project 엔티티
        //study 엔티티
        return "index";
    }
}
