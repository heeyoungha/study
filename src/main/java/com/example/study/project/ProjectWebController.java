package com.example.study.project;

import com.example.study.project.dto.ProjectRequest;
import com.example.study.project.dto.ProjectResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.data.web.PageableDefault;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Controller
@RequestMapping("/project")
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

    @PostMapping("/create")
    public String createProject(@ModelAttribute ProjectRequest.CreateProjectRequest request) {
        projectService.saveProject(request);
        return "redirect:/project";
    }

    @GetMapping("/api/project")
    @ResponseBody
    public ResponseEntity<Map<String, Object>> getProjects(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size,
            @RequestParam(required = false) String searchKeyword,
            @RequestParam(required = false) String quarterFilter,
            @RequestParam(required = false) String statusFilter) {
        
        Pageable pageable = PageRequest.of(page, size, Sort.by("id").descending());
        Page<ProjectResponse> projectPage = projectService.readProjectListWithFilters(
            searchKeyword, quarterFilter, statusFilter, pageable);
        
        Map<String, Object> response = new HashMap<>();
        response.put("content", projectPage.getContent());
        response.put("last", projectPage.isLast());
        response.put("totalElements", projectPage.getTotalElements());
        response.put("totalPages", projectPage.getTotalPages());
        
        return ResponseEntity.ok(response);
    }

    @GetMapping("/{id}")
    public String readProject(@PathVariable Long id, Model model) {
        ProjectResponse response = projectService.readProject(id);
        model.addAttribute("project", response);
        return "project/project-detail";
    }

    @GetMapping("/{id}/edit")
    public String editProject(@PathVariable Long id, Model model) {
        ProjectResponse response = projectService.readProject(id);
        model.addAttribute("project", response);
        return "project/project-form"; // create와 동일 폼 사용
    }

    @PostMapping("/{id}/delete")
    public String deleteProject(@PathVariable Long id) {
        projectService.deleteProject(id);
        return "redirect:/project/list"; // 삭제 후 목록 페이지로 이동
    }
   
}