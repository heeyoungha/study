package com.example.study.cafe.controller;

import com.example.study.cafe.dto.InputDto;
import com.example.study.cafe.dto.OutputDto;
import com.example.study.cafe.service.CafeRecommendationService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;

import java.util.List;

@Controller
@RequestMapping("/v1")
@RequiredArgsConstructor
public class FormController {

    private final CafeRecommendationService cafeRecommendationService;

    @GetMapping("/main")
    public String main(){
        return "main";
    }

    @PostMapping("/search")
    public String postDirection(@ModelAttribute InputDto inputDto, Model model) {

        List<OutputDto> recommendedCafes = cafeRecommendationService.recommendCafeList(inputDto.getAddress());

        // 모델에 데이터를 추가합니다.
        model.addAttribute("outputFormList", recommendedCafes);

        // 결과를 보여줄 타임리프 HTML 템플릿의 이름을 반환합니다.
        return "output";
    }
}
