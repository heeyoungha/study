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
import org.springframework.web.bind.annotation.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import com.example.study.user.User;
import com.example.study.user.UserRepository;

import java.util.List;

@RestController
@RequiredArgsConstructor
@RequestMapping("/api/project")
public class ProjectApiController {
    private final ProjectService projectService;
    private final UserRepository userRepository;

    private static final Logger logger = LoggerFactory.getLogger(ProjectApiController.class);


    @PostMapping
    public ResponseEntity<ProjectResponse> createProject(@RequestBody ProjectRequest.CreateProjectRequest request){
        // SecurityContext에서 사용자 정보 가져오기
        Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
        String username = authentication.getName();
        
        User user = userRepository.findByUsername(username);
        if (user == null) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).build();
        }
        
        request.setUserId(user.getId());

        ProjectResponse response = projectService.saveProject(request);
        return ResponseEntity.ok(response);
    }

    @GetMapping
    public ResponseEntity<Page<ProjectResponse>> readProjectList(@PageableDefault(page = 0, size = 5, sort = "id", direction = Sort.Direction.DESC)
                                                                     Pageable pageable,
                                                                 @RequestParam(required = false) String searchKeyword){
        Page<ProjectResponse> response = projectService.readProjectList(searchKeyword, pageable);
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
