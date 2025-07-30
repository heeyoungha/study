package com.example.study.project;

import com.example.study.board.Board;
import com.example.study.project.dto.ProjectRequest;
import com.example.study.project.dto.ProjectResponse;
import com.example.study.user.User;
import com.example.study.user.UserRepository;
import com.example.study.common.ServiceUtil;
import com.example.study.common.exception.DomainException;
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
        // 선택된 월들로부터 분기 계산
        String quarters = calculateQuarters(request.getTargetMonths());
        
        Project project = Project.of(
            request.getTitle(), 
            request.getTimeZone(), 
            request.getTargetMonths(), 
            quarters,
            request.getPlace(), 
            request.getStatus()
        );
        projectRepository.save(project);
        return new ProjectResponse(project);
    }

    // 선택된 월들로부터 분기 계산하는 메서드
    private String calculateQuarters(String targetMonths) {
        if (targetMonths == null || targetMonths.trim().isEmpty()) {
            return "";
        }
        
        String[] months = targetMonths.split(",");
        java.util.Set<String> quarters = new java.util.HashSet<>();
        
        for (String month : months) {
            month = month.trim();
            if (month.contains("월")) {
                month = month.replace("월", "");
            }
            
            try {
                int monthNum = Integer.parseInt(month);
                if (monthNum >= 1 && monthNum <= 12) {
                    if (monthNum <= 3) {
                        quarters.add("1분기");
                    } else if (monthNum <= 6) {
                        quarters.add("2분기");
                    } else if (monthNum <= 9) {
                        quarters.add("3분기");
                    } else {
                        quarters.add("4분기");
                    }
                }
            } catch (NumberFormatException e) {
                // 숫자가 아닌 경우 무시
            }
        }
        
        return String.join(",", quarters);
    }


    public Page<ProjectResponse> readProjectList(String searchTitle, Pageable pageable) {

        Page<ProjectResponse> projcetList = projectRepository.findAll(pageable).map(ProjectResponse::new);

        if(searchTitle == null) {
            return projcetList;
        }

        Page<Project> projects = projectRepository.findByTitleContaining(searchTitle, pageable);

        return projects.map(ProjectResponse::new);
    }

    public Page<ProjectResponse> readProjectListWithFilters(String searchKeyword, String quarterFilter, String statusFilter, Pageable pageable) {
        List<Project> allProjects = projectRepository.findAll();
        
        // 필터링 적용
        List<Project> filteredProjects = allProjects.stream()
            .filter(project -> {
                // 검색어 필터
                if (searchKeyword != null && !searchKeyword.trim().isEmpty()) {
                    if (!project.getTitle().toLowerCase().contains(searchKeyword.toLowerCase())) {
                        return false;
                    }
                }
                
                // 분기 필터
                if (quarterFilter != null && !quarterFilter.trim().isEmpty()) {
                    if (project.getQuarters() == null || !project.getQuarters().contains(quarterFilter)) {
                        return false;
                    }
                }
                
                // 상태 필터
                if (statusFilter != null && !statusFilter.trim().isEmpty()) {
                    if (!statusFilter.equals(project.getStatus())) {
                        return false;
                    }
                }
                
                return true;
            })
            .collect(Collectors.toList());
        
        // 페이지네이션 적용
        int start = (int) pageable.getOffset();
        int end = Math.min(start + pageable.getPageSize(), filteredProjects.size());
        
        List<Project> pageContent = filteredProjects.subList(start, end);
        Page<Project> projectPage = new PageImpl<>(pageContent, pageable, filteredProjects.size());
        
        return projectPage.map(ProjectResponse::new);
    }

    public ProjectResponse readProject(Long id) {
        Project project = ServiceUtil.findByIdOrThrow(projectRepository, id, DomainException.notFindRow(id));
        ProjectResponse response = new ProjectResponse(project);

        return response;
    }

    public void deleteProject(Long id) {
        Project project = ServiceUtil.findByIdOrThrow(projectRepository, id, DomainException.notFindRow(id));
        project.delete();
    }

    public ProjectResponse updateProject(Long id, ProjectRequest.UpdateProjectRequest request) {
        Project project = ServiceUtil.findByIdOrThrow(projectRepository, id, DomainException.notFindRow(id));

        // 선택된 월들로부터 분기 계산
        String quarters = calculateQuarters(request.getTargetMonths());
        
        project.updateProject(
            request.getTitle(), 
            request.getTimeZone(), 
            request.getTargetMonths(), 
            quarters,
            request.getPlace(),
            request.getStatus()
        );
        
        return new ProjectResponse(project);
    }
}
