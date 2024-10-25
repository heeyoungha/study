package com.example.study.project;

import com.example.study.project.dto.ProjectRequest;
import com.example.study.project.dto.ProjectResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@Controller
@RequestMapping("/v1/project")
public class ProjectWebController {

    @GetMapping
    public String projectList() {
        return "project/project-list";
    }

    @GetMapping("/create")
    public String createProject() {
        return "project/project-form";
    }

}