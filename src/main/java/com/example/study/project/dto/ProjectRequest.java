package com.example.study.project.dto;

import lombok.Data;

public class ProjectRequest {

    @Data
    public static class CreateProjectRequest{

        private String title;
        private String startDate;
        private Long userId;

    }

    @Data
    public static class UpdateProjectRequest{
        private String title;
        private String startDate;
    }
}
