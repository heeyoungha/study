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
    private String status;
    private String place;

    public ProjectResponse(Project project){

        this.id = project.getId();
        this.title = project.getTitle();
        this.startDate = project.getStartDate();
        this.status = project.getStatus();
        this.place = project.getPlace();
    }
}
