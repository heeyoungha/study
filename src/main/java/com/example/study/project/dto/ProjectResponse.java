package com.example.study.project.dto;

import com.example.study.project.Project;
import lombok.Data;
import org.springframework.boot.autoconfigure.info.ProjectInfoProperties;

@Data
public class ProjectResponse {

    private Long id;
    private String title;
    private String startDate;
    private String userName;

    public ProjectResponse(Project project){

        this.id = project.getId();
        this.title = project.getTitle();
        this.startDate = project.getStartDate();
    }
}
