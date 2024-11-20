package com.example.study.project;

import com.example.study.project.dto.ProjectRequest;
import com.example.study.project.dto.ProjectResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.data.web.PageableDefault;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@Controller
@RequestMapping("/v1/project")
@RequiredArgsConstructor
public class ProjectWebController {

    private final ProjectService projectService;

    @GetMapping
    public String projectList(Model model,
                              @PageableDefault(page = 0, size = 5, sort = "id", direction = Sort.Direction.DESC)
                              Pageable pageable,
                              @RequestParam(required = false) String searchKeyword) {
        Page<ProjectResponse> projectPage = projectService.readProjectList(searchKeyword, pageable);

        int nowPage = projectPage.getPageable().getPageNumber() + 1; //pageable에서 넘어온 현재페이지를 가지고올수있다 * 0부터시작하니까 +1
        int startPage = Math.max(nowPage - 4, 1); //매개변수로 들어온 두 값을 비교해서 큰값을 반환
        int endPage = Math.min(nowPage + 5, projectPage.getTotalPages());


        model.addAttribute("projectList" , projectPage);
        model.addAttribute("nowPage", nowPage);
        model.addAttribute("startPage", startPage);
        model.addAttribute("endPage", endPage);
        model.addAttribute("searchKeyword", searchKeyword);

        return "project/project-list";
    }

    @GetMapping("/create")
    public String createProject() {
        return "project/project-form";
    }

}