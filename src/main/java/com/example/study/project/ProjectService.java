package com.example.study.project;

import com.example.study.project.dto.ProjectRequest;
import com.example.study.project.dto.ProjectResponse;
import com.example.study.user.User;
import com.example.study.user.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class ProjectService {

    private final UserRepository userRepository;
    private final ProjectRepository projectRepository;


    @Transactional
    public ProjectResponse saveProject(ProjectRequest.CreateProjectRequest request) {


        Project project = Project.of(request.getTitle(), request.getStartDate());
        projectRepository.save(project);
        return new ProjectResponse(project);
    }

    @Transactional
    public List<ProjectResponse> readProjectList() {
        return projectRepository.findAll().stream().map(ProjectResponse::new).collect(Collectors.toList());
    }

    @Transactional
    public ProjectResponse readProject(Long id) {
        Project project = projectRepository.findById(id).orElseThrow();
        ProjectResponse response = new ProjectResponse(project);

        return response;
    }

    @Transactional
    public void deleteProject(Long id) {
        Project project = projectRepository.findById(id).orElseThrow();
        project.delete();
    }

    @Transactional
    public void updateProject(Long id, ProjectRequest.UpdateProjectRequest request) {
        Project project = projectRepository.findById(id).orElseThrow();

        project.updateProject(request.getTitle(), request.getStartDate());
    }
}
