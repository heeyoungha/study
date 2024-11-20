package com.example.study.project;

import com.example.study.board.Board;
import com.example.study.project.dto.ProjectRequest;
import com.example.study.project.dto.ProjectResponse;
import com.example.study.user.User;
import com.example.study.user.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
@Transactional
public class ProjectService {

    private final UserRepository userRepository;
    private final ProjectRepository projectRepository;


    public ProjectResponse saveProject(ProjectRequest.CreateProjectRequest request) {


        Project project = Project.of(request.getTitle(), request.getStartDate());
        projectRepository.save(project);
        return new ProjectResponse(project);
    }


    public Page<ProjectResponse> readProjectList(String searchTitle, Pageable pageable) {

        Page<ProjectResponse> projcetList = projectRepository.findAll(pageable).map(ProjectResponse::new);

        if(searchTitle == null) {
            return projcetList;
        }

        Page<Project> projects = projectRepository.findByTitleContaining(searchTitle, pageable);

        return projects.map(ProjectResponse::new);





    }

    public ProjectResponse readProject(Long id) {
        Project project = projectRepository.findById(id).orElseThrow();
        ProjectResponse response = new ProjectResponse(project);

        return response;
    }

    public void deleteProject(Long id) {
        Project project = projectRepository.findById(id).orElseThrow();
        project.delete();
    }

    public void updateProject(Long id, ProjectRequest.UpdateProjectRequest request) {
        Project project = projectRepository.findById(id).orElseThrow();

        project.updateProject(request.getTitle(), request.getStartDate());
    }
}
