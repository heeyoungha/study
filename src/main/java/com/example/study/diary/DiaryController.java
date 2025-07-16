package com.example.study.diary;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.*;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;
import java.util.*;

@Controller
@RequestMapping("/diary")
public class DiaryController {

    @Value("${fastapi.url:http://python-api:8000/diary}")
    private String fastApiUrl;

    @GetMapping("")
    public String diaryForm() {
        return "diary/diary-form";
    }

    @PostMapping("")
    public String submitDiary(@RequestParam("text") String text, Model model) {
        RestTemplate restTemplate = new RestTemplate();
        Map<String, String> request = new HashMap<>();
        request.put("text", text);
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        HttpEntity<Map<String, String>> entity = new HttpEntity<>(request, headers);
        try {
            ResponseEntity<Map> response = restTemplate.postForEntity(fastApiUrl, entity, Map.class);
            model.addAttribute("sentiment", response.getBody().get("sentiment"));
            model.addAttribute("recommendations", response.getBody().get("recommendations"));
        } catch (Exception e) {
            model.addAttribute("error", "FastAPI 서버와 통신에 실패했습니다.");
        }
        model.addAttribute("text", text);
        return "diary/diary-result";
    }
} 