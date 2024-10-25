package com.example.study.project;

import com.example.study.project.dto.ProjectRequest;
import com.example.study.project.dto.ProjectResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import jakarta.servlet.http.HttpSession;

import java.util.List;

@RestController
@RequiredArgsConstructor
@RequestMapping("/v1/api/project")
public class ProjectApiController {
    private final ProjectService projectService;

    private static final Logger logger = LoggerFactory.getLogger(ProjectApiController.class);


    @PostMapping
    public ResponseEntity<ProjectResponse> createProject(@RequestBody ProjectRequest.CreateProjectRequest request, HttpSession session){
        // 세션에서 userId 가져오기
        Long userId = (Long) session.getAttribute("userId");
        request.setUserId(userId);

        ProjectResponse response = projectService.saveProject(request);
        return ResponseEntity.ok(response);
    }

    @GetMapping
    public ResponseEntity<List<ProjectResponse>> readProjectList(){
        List<ProjectResponse> response = projectService.readProjectList();
        return ResponseEntity.ok(response);
    }

    @GetMapping("/{id}")
    public ResponseEntity<ProjectResponse> readProject(@PathVariable Long id){
        ProjectResponse response = projectService.readProject(id);
        return ResponseEntity.ok(response);
    }

    @PutMapping("/{id}")
    public ResponseEntity<?> updateProject(
            @PathVariable Long id,
            @RequestBody ProjectRequest.UpdateProjectRequest request) {

            projectService.updateProject(id, request);
            return ResponseEntity.status(HttpStatus.OK).build();
    }
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteProject(@PathVariable Long id){
        projectService.deleteProject(id);
        return ResponseEntity.status(HttpStatus.NO_CONTENT).build();
    }
}
